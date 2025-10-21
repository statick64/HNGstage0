from django.urls import path
from .views import SentenceView

#/me url pattern 
urlpatterns = [
    path('strings', SentenceView.as_view()),
]