HNG STAGE 0

🚀 API Response
{
  "status": "success",
  "user": {
    "email": "kokoeteisong@gmail.com",
    "name": "Kpongete Isong",
    "stack": "Django (Python)"
  },
  "timestamp": "2025-10-17T09:01:13.562738+00:00",
  "fact": "Cats sleep for around 13 to 14 hours a day."
}

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/statick64/HNGstage0

cd into cloned repo

Create and activate a virtual environment

run python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows


run pip install -r requirements.txt 


run python manage.py runserver

🌐 API Endpoint
Method	Endpoint	Description
GET	/api/user-info/	Returns status, user info, datetinme  and cat fact

🧠 How It Works

The view in views.py:

Fetches the first user record from the database

Serializes it using DeveloperSerializer

Makes a live HTTP request to https://catfact.ninja/fact to get a random cat fact

Returns all of that in a structured JSON format with a UTC timestamp

🧩 Tech Stack

Python 3.x

Django 5+

Django REST Framework (DRF)

Requests (for external API calls)

Enviroment vairable
SECRET_KEY = 'django-insecure-#__-9pf+a0n!vfk4#qid$nrouslbd0b%dq7qh&8t#3gr68@duh' 

🧪 Test

You can test the endpoint directly with curl or a browser:

curl https://enchanting-eagerness-production.up.railway.app/me