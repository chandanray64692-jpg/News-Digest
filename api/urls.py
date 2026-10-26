from django.urls import path
from . import views

urlpatterns = [
    path("intelligence-feed/", views.intelligence_feed, name="intelligence_feed"),
    path("dashboard-stats/", views.dashboard_stats, name="dashboard_stats"),
    path("country-stats/", views.country_stats, name="country_stats"),
    path("priority-stats/", views.priority_stats, name="priority_stats"),
    path("latest-alerts/", views.latest_alerts, name="latest_alerts"),
    path("ai-prediction/", views.ai_prediction, name="ai_prediction"),
    path("daily-sitrep/", views.daily_sitrep, name="daily_sitrep"),
]