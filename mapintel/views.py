from django.shortcuts import render
from intelligence.models import IntelligenceArticle
from django.http import JsonResponse

def map_points(request):
    return JsonResponse([
        {
            "id": 1,
            "title": "Test India Intelligence",
            "country": "India",
            "lat": 20.5937,
            "lon": 78.9629,
            "priority": "HIGH",
            "threat": 80
        }
    ], safe=False)
def country_intel(request):

    country=request.GET.get("country")

    data=[]

    articles=IntelligenceArticle.objects.filter(
        country__name=country
    ).order_by("-id")[:50]

    for a in articles:

        data.append({

        "title":a.title,

        "summary":a.summary,

        "priority":a.priority,

        "threat":a.threat_score

        })

    return JsonResponse({
        "articles":data
    })
from django.shortcuts import render

def world_map(request):

    return render(
        request,
        "mapintel/world_map.html"
    )
from django.http import JsonResponse
from intelligence.models import IntelligenceArticle


def map_points(request):
    COUNTRY_COORDS = {
        "India": [20.5937, 78.9629],
        "Pakistan": [30.3753, 69.3451],
        "China": [35.8617, 104.1954],
        "Russia": [61.5240, 105.3188],
        "Ukraine": [48.3794, 31.1656],
        "United States": [37.0902, -95.7129],
        "USA": [37.0902, -95.7129],
        "Israel": [31.0461, 34.8516],
        "Iran": [32.4279, 53.6880],
        "Afghanistan": [33.9391, 67.7100],
        "Bangladesh": [23.6850, 90.3563],
        "Sri Lanka": [7.8731, 80.7718],
        "Nepal": [28.3949, 84.1240],
        "Myanmar": [21.9162, 95.9560],
        "Japan": [36.2048, 138.2529],
        "France": [46.2276, 2.2137],
        "Germany": [51.1657, 10.4515],
        "United Kingdom": [55.3781, -3.4360],
        "Canada": [56.1304, -106.3468],
        "Australia": [-25.2744, 133.7751],
    }

    def get_country_name(country):
        if not country:
            return "Global"

        if hasattr(country, "name"):
            return country.name

        return str(country)

    def get_threat_score(priority):
        priority = str(priority).upper()

        if priority == "CRITICAL":
            return 95
        if priority == "HIGH":
            return 80
        if priority == "MEDIUM":
            return 50

        return 20

    points = []

    articles = IntelligenceArticle.objects.all().order_by("-id")[:500]

    for article in articles:
        country = get_country_name(article.country)

        if country not in COUNTRY_COORDS:
            continue

        lat, lon = COUNTRY_COORDS[country]
        threat = get_threat_score(article.priority)

        points.append({
            "id": article.id,
            "title": article.title,
            "country": country,
            "lat": lat,
            "lon": lon,
            "priority": article.priority,
            "threat": threat,
        })

    return JsonResponse(points, safe=False)
from django.http import JsonResponse
from intelligence.models import IntelligenceArticle


def latest_world_news(request):

    articles = IntelligenceArticle.objects.all().order_by("-id")[:30]

    data = []

    for a in articles:

        data.append({
            "title": a.title,
            "country": str(a.country) if a.country else "Global",
            "priority": a.priority,
            "summary": a.summary[:200],
        })

    return JsonResponse({
        "articles": data
    })