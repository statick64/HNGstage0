from django.urls import path
from .views import SentencePostAndFilterView, SentenceGetAndDeleteView, SentenceNaturalLanguageFilterView

#/me url pattern 
urlpatterns = [
    path('strings', SentencePostAndFilterView.as_view(), name='sentence-post-and-filter'),
    path("strings/{<str:string_value>}", SentenceGetAndDeleteView.as_view(), name="sentence-detail-and-delete"),
    path('strings/filter-by-natural-language', SentenceNaturalLanguageFilterView.as_view(), name='sentence-nl-filter'),
    
]