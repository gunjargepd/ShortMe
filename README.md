# ShortMe


Welcome to ShortMe, where we simplify the web one link at a time! Our URL shortening service is designed to make your links manageable and easy to share. Say goodbye to long, complicated URLs and hello to concise, user-friendly links that retain the essence of your message.

To try out in action, visit [https://shortme.co.in](https://shortme.co.in) 

### Core Idea:
ShortMe addresses the inconvenience of lengthy URLs by providing a user-friendly platform to shorten them, simplifying sharing and improving digital communication.

### Problem Being Addressed:
Cumbersome URLs hinder effective communication and user experience. ShortMe resolves this by offering a solution to shorten URLs, making them more manageable for sharing and eliminating associated errors and frustration.

### How the Problem is Being Solved:
ShortMe simplifies the sharing process by allowing users to input long URLs and generating concise alternatives. This ensures accurate communication and a more efficient user experience, alleviating the challenges of dealing with lengthy web addresses.

### Addressing a Clear Need:
In a digital age, where sharing information is constant, ShortMe fulfills the need for an efficient and user-friendly URL management solution, providing a straightforward way to handle lengthy URLs.

### Mapped Purpose and Basic Functionality:
The purpose of ShortMe aligns with the problem of cumbersome URLs. Its basic functionality involves users inputting a long URL, and ShortMe generates a shortened version, directly addressing the challenge of lengthy URLs hindering efficient online communication.


Follwoing are few screenshot

![Screenshot](/static/screenshots/login.png)

![Screenshot](/static/screenshots/index.png)

![Screenshot](/static/screenshots/links.png)

![Screenshot](/static/screenshots/link_details.png)

![Screenshot](/static/screenshots/contact.png)


## To Run

Create a virtual environment

``` sh
python -m venv env
```

Activate the environment

For windows
```sh
env\Scripts\activate
```

For linux
``` sh
source env/bin/activate
```

Install dependencies

```sh
pip install -r requirements.txt
```

Go to shortme folder

``` sh
cd shortme
```

Create .env file refer [.env.example](/shortme/.env.example)

Come back to root folder of project

``` sh
cd ..
```


Make migrations for database

``` sh
python manage.py makemigrations
```

Migrate

``` sh
python manage.py migrate
```

Create the superuser (optional)

``` sh
python manage.py createsuperuser
```

Run the Server

``` sh
python manage.py runserver
```