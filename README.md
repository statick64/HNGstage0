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

🧱 Project Structure


settings.py Setup
INSTALLED_APPS = [
    'api',
    'rest_framework',
]


models.py Setup
User model:
    email="you@example.com",
    name="Your Name",
    stack="Django (Python)"



Run the server

python manage.py runserver

🌐 API Endpoint
Method	Endpoint	Description
GET	/me	Returns success, user info, datetime and cat fact
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

🧪 Test

You can test the endpoint directly with curl or a browser:

curl http://127.0.0.1:8000/api/user-info/