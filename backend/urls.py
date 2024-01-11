from django.urls import path
from backend.views import (index, signin, register, signout, 
                           create_link, edit_link, links, delete_link, link_details, 
                           getslug, contact)

appname = "backend"

urlpatterns = [
    path("", index, name="index"),
    path("login/", signin, name="signin"),
    path("register/", register, name="register"),
    path("logout/", signout, name="signout"),
    path("createlink/", create_link, name="create_link"),
    path("editlink/<uuid:lid>", edit_link, name="edit_link"),
    path("deletelink/<uuid:lid>", delete_link, name="delete_link"),
    path("links/", links, name="links"),
    path("linkdetails/<uuid:lid>", link_details, name="link_details"),
    path("contact/", contact, name="contact"),

    # keep this url at th end
    path("<slug:slug>", getslug, name="getslug"),
]