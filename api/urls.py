from django.urls import path
from . import views

#/me url pattern 
urlpatterns = [
    path('me', views.getData),
]