from django.urls import path
from . import views

urlpatterns = [
    path("world-map/", views.world_map, name="world_map"),
    path("api/country-news/", views.country_intel, name="country_news"),
    path("api/map-points/", views.map_points, name="map_points"),
    path("api/latest-news/",views.latest_world_news,name="latest_news"),
    

]