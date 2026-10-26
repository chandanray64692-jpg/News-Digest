from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),

    # Dashboard / Home
    path('', include('core.urls')),

    # APIs
    path('api/', include('api.urls')),

    # Modules
    path('mapintel/', include('mapintel.urls')),
    path('analytics/', include('analytics.urls')),
    path('reports/', include('reports.urls')),
    path('ai/', include('ai_engine.urls')),
    path('realtime/', include('realtime.urls')),
    path('collectors/', include('collectors.urls')),
    path('notifications/', include('notifications.urls')),

]

# Media Files
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)