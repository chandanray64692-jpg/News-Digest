from django.http import JsonResponse

from .rss_collector import collect_rss

from .newsapi_collector import fetch_newsapi

from .gnews_collector import fetch_gnews

from .rss_collector import save_article


def fetch_now(request):

    imported=0

    imported+=collect_rss()

    for a in fetch_newsapi():

        title=a.get("title","")
        summary=a.get("description","")

        if save_article(
            title,
            summary,
            "NewsAPI"
        ):
            imported+=1

    for a in fetch_gnews():

        title=a.get("title","")
        summary=a.get("description","")

        if save_article(
            title,
            summary,
            "GNews"
        ):
            imported+=1

    return JsonResponse({

        "status":"success",

        "imported":imported

    })
from django.http import JsonResponse

from .orchestrator import collect_all_news

def fetch_now(request):

    total = collect_all_news()

    return JsonResponse({

        "status":"success",

        "imported":total

    })
from django.http import JsonResponse

from .rss_collector import collect_rss


def fetch_now(request):

    total = collect_rss()

    return JsonResponse({

        "status": "success",

        "imported": total

    })
from django.http import JsonResponse
from .rss_collector import collect_rss

def fetch_now(request):

    count=collect_rss()

    return JsonResponse({

        "status":"ok",

        "imported":count

    })
from ai_engine.analyzer import analyze_article
from intelligence.models import IntelligenceArticle


def analyze_all_news(request):

    count = 0

    for article in IntelligenceArticle.objects.all():

        analyze_article(article)

        count += 1

    return JsonResponse({
        "analyzed": count
    })
from django.http import JsonResponse
from .twitter_collector import collect_twitter_intel


def fetch_twitter_now(request):
    imported = collect_twitter_intel()

    return JsonResponse({
        "status": "success",
        "imported": imported
    })
from django.http import JsonResponse

def collectors_home(request):
    return JsonResponse({
        "message": "IDIGAS Collectors API",
        "available_urls": [
            "/collectors/fetch-now/",
            "/collectors/analyze-news/",
            "/collectors/fetch-twitter/"
        ]
    })
from django.shortcuts import render

def collectors_home(request):
    return render(request, "collectors/index.html")