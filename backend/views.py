from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators  import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseNotFound
from backend.models import Link, Feedback
import segno 
import io
from django.core.files.base import ContentFile
from shortme.settings import BASE_DIR, BASE_PREFIX
from backend.utils import analyze_text
from os import path
import string
import random


# Create your views here.

charset = string.ascii_letters + string.digits

static_dir = path.join(BASE_DIR, "static")

def register(request):
    if request.method =="POST":
        form = request.POST

        first_name = form.get("fname", "")
        last_name = form.get("lname", "")
        email = form.get("email", "")
        username = form.get("uname", "")
        password = form.get("password", "")
        confirm_password = form.get("confirm_password", "")

        if "" in (first_name, last_name, email, username, password, confirm_password):
            messages.add_message(request, messages.ERROR, "All fields are required!")
        else:
            if password != confirm_password:
                messages.add_message(request, messages.ERROR, "Password mismatch!")
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                messages.add_message(request, messages.SUCCESS, "User created successfully!")
                return redirect(signin)
    else:
        try:
            if request.user.is_authenticated:
                return redirect(index)
        except Exception as e:
            print(e)
    return render(request,'register.html')

def signin(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect(index)
        else:
            messages.add_message(request,messages.ERROR,"Incorrect username or password!")

    else:
        try:
            if request.user.is_authenticated:
                return redirect(index)
        except Exception as e:
            messages.add_message(request,messages.ERROR,str(e))
    return render(request,'login.html')

@login_required(login_url='/login/')
def signout(request):
    logout(request)
    return redirect(signin)

@login_required(login_url='/login/')
def index(request):
    user = request.user

    links = Link.objects.filter(user=user).all()

    return render(request,'index.html',{'user':user, "links": links} )  


@login_required(login_url ='/login/')
def links(request):
    user = request.user

    links = Link.objects.filter(user=user).all()

    return render(request, "links.html", {"user":user,"links": links}) 


@login_required(login_url ='/login/')
def link_details(request, lid):

    user = request.user

    link = get_object_or_404(Link, id=lid)

    if link.user != user:
        messages.add_message(request, messages.ERROR, "Unauthorized access!")
        return redirect(links)
    
    return render(request, "link_details.html", {"link": link})


@login_required(login_url ='/login/')
def create_link(request):

    user = request.user

    if request.method == "POST":

        form = request.POST

        name = form.get("name","")
        suffix =form.get("suffix","")
        url = form.get("url","")
        limit =form.get("limit","")

        submitted_data = {
            "name": name,
            "suffix": suffix,
            "url": url,
            "limit": limit
        }

        if "" in[name,suffix,url]:
            messages.add_message(request, messages.ERROR, "Bad request!")
            return render(request, "create_link.html", submitted_data)

        limit = int(limit) if limit else 0

        link = Link.objects.filter(suffix=suffix).first()

        if link:
            messages.add_message(request, messages.ERROR, "suffix already exist, please choose something else!")
            return render(request, "create_link.html", submitted_data)
        
        secure, categories = analyze_text(f"{suffix} {url}")

        if not secure:
            for c in categories:
                messages.add_message(request, messages.ERROR, f"Violation of policy detected! {c} content found!")
            return render(request, "create_link.html", submitted_data)
        
        link = Link.objects.create(suffix=suffix, user=user, name=name, url=url, limit=limit)

        qrcode = segno.make(f"{BASE_PREFIX}/{suffix}")
        out = io.BytesIO()
        qrcode.save(out, kind='png', dark='#00008b', light=None, scale=10)

        link.qrcode.save(f'{link.id}.png', ContentFile(out.getvalue()), save=False)

        link.save()

        return redirect(links)
    
    s = "".join(random.choices(charset, k=8))

    return render(request, "create_link.html", {"suffix": s})


@login_required(login_url ='/login/')
def edit_link(request, lid):

    user = request.user

    link = get_object_or_404(Link, id=lid)

    if link.user != user:
        messages.add_message(request, messages.ERROR, "Unauthorized access!")
        return redirect(links)
    
    if request.method == "POST":

        form = request.POST

        name = form.get("name","")
        suffix =form.get("suffix","")
        url = form.get("url","")
        limit =form.get("limit","")

        if "" in[name,suffix,url]:
            messages.add_message(request, messages.ERROR, "Bad request!")
            return render(request, "edit_link.html", {"link": link})
        
        secure, categories = analyze_text(f"{suffix} {url}")

        if not secure:
            for c in categories:
                messages.add_message(request, messages.ERROR, f"Violation of policy detected! {c} content found!")
            return render(request, "edit_link.html", {"link": link})
        
        limit = int(limit) if limit else 0

        if link.name != name:
            link.name = name

        if link.suffix != suffix:
            link.suffix = suffix

            qrcode = segno.make(f"{BASE_PREFIX}/{suffix}")
            out = io.BytesIO()
            qrcode.save(out, kind='png', dark='#00008b', light=None, scale=10)

            link.qrcode.save(f'{link.id}.png', ContentFile(out.getvalue()), save=False)

        if link.url != url:
            link.url = url

        if link.limit != limit:
            link.limit = limit

        link.save()

        messages.add_message(request, messages.SUCCESS, "Link edited uccesfully!")

        return redirect(links)
    
    return render(request, "edit_link.html", {"link": link})


@login_required(login_url ='/login/')
def delete_link(request, lid):

    user = request.user

    link = get_object_or_404(Link, id=lid)

    if link.user == user:
        link.delete()
        messages.add_message(request, messages.SUCCESS, "Link deleted succesfully!")
    else:  
        messages.add_message(request, messages.ERROR, "Unauthorized access!")

    return redirect(links)


def getslug(rquest, slug):
    
    link = Link.objects.filter(suffix=slug).first()

    if link:
        link.visit += 1
        link.save()
        return redirect(link.url)
    else:
        return HttpResponseNotFound("Url does not exist")



def contact(request):

    user = request.user

    if request.method == "POST":

        form = request.POST

        name = form.get("name", "")
        email = form.get("email", "")
        message = form.get("message", "")

        if not "" in (name, email):
            
            Feedback.objects.create(name=name, email=email, message=message)
            messages.add_message(request, messages.SUCCESS, "Thank you for feedback!")

        else:
            messages.add_message(request, messages.ERROR, "Unexpected error!")


    return render(request, "contact.html")
