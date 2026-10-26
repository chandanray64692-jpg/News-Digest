from django.http import JsonResponse
from .services import *

def analyze_text(request):

    text=request.GET.get("text","")

    return JsonResponse({

    "country":
    detect_country(text),

    "category":
    detect_category(text),

    "threat":
    threat_score(text),

    "summary":
    generate_summary(text)

    })