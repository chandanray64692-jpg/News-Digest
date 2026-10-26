from django.urls import path
from . import views

urlpatterns = [
    path("fetch-now/", views.fetch_now, name="fetch_now"),
    path("analyze-news/", views.analyze_all_news, name="analyze_news"),
    path("fetch-twitter/", views.fetch_twitter_now, name="fetch_twitter"),
    path("", views.collectors_home, name="collectors_home"),
    
]