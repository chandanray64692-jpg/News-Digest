from django.urls import path
from .views import *

urlpatterns=[

path(
'stats/',
dashboard_stats
),

path(
'intelligence-feed/',
intelligence_feed
),

path(
'country-stats/',
country_stats
),

path(
'priority-stats/',
priority_stats
),

path(
'latest-alerts/',
latest_alerts
),

]