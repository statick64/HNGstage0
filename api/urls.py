from django.urls import path
from .views import SentencePostView, SentenceGetView

#/me url pattern 
urlpatterns = [
    path('strings', SentencePostView.as_view()),
    path("strings/<str:string_value>/", SentenceGetView.as_view(), name="sentence-detail"),
]