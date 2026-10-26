from django.http import JsonResponse
from .models import *

def active_alerts(request):

    data=[]

    alerts=Alert.objects.filter(
    active=True
    ).order_by("-created_at")

    for a in alerts:

        data.append({

        "id":a.id,

        "title":a.title,

        "message":a.message,

        "level":a.level,

        "time":a.created_at.strftime(
        "%d-%m-%Y %H:%M"
        )

        })

    return JsonResponse({
    "alerts":data
    })