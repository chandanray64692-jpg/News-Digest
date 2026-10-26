from django.urls import path
from . import views

urlpatterns = [
    path("", views.analytics_page, name="analytics"),
    path("threat-radar/", views.threat_radar_page, name="threat_radar"),
]