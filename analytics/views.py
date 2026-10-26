from django.http import JsonResponse
from intelligence.models import *
from django.db.models import Count,Avg
from datetime import datetime,timedelta

def threat_trends(request):

    data=[]

    for i in range(7):

        day=datetime.now()-timedelta(days=i)

        score=IntelligenceArticle.objects.filter(
        published_date__date=day.date()
        ).aggregate(avg=Avg('threat_score'))

        data.append({
        "date":day.strftime("%d-%m"),
        "score":score['avg'] or 0
        })

    return JsonResponse({"trend":data[::-1]})


def category_distribution(request):

    data=[]

    for c in Category.objects.all():

        total=IntelligenceArticle.objects.filter(
        category=c
        ).count()

        data.append({
        "category":c.name,
        "count":total
        })

    return JsonResponse({"categories":data})


def top_countries(request):

    data=[]

    for c in Country.objects.all():

        count=IntelligenceArticle.objects.filter(
        country=c
        ).count()

        data.append({
        "country":c.name,
        "count":count
        })

    data=sorted(
    data,
    key=lambda x:x["count"],
    reverse=True
    )

    return JsonResponse({
    "countries":data[:10]
    })


def top_sources(request):

    data=[]

    for s in NewsSource.objects.all():

        count=IntelligenceArticle.objects.filter(
        source=s
        ).count()

        data.append({
        "source":s.name,
        "count":count
        })

    data=sorted(
    data,
    key=lambda x:x["count"],
    reverse=True
    )

    return JsonResponse({
    "sources":data[:10]
    })


def dashboard_analytics(request):

    return JsonResponse({

    "articles":
    IntelligenceArticle.objects.count(),

    "countries":
    Country.objects.count(),

    "sources":
    NewsSource.objects.count(),

    "critical":
    IntelligenceArticle.objects.filter(
    priority="CRITICAL"
    ).count(),

    "high":
    IntelligenceArticle.objects.filter(
    priority="HIGH"
    ).count()

    })
from django.shortcuts import render
from django.http import JsonResponse
from intelligence.models import IntelligenceArticle


def analytics_page(request):
    articles = IntelligenceArticle.objects.all().order_by("-id")[:300]
    return render(request, "analytics/analytics.html", {"articles": articles})


def threat_radar_page(request):
    articles = IntelligenceArticle.objects.filter(
        priority__in=["HIGH", "CRITICAL"]
    ).order_by("-id")[:200]

    return render(request, "analytics/threat_radar.html", {"articles": articles})


def analytics_data(request):
    total = IntelligenceArticle.objects.count()

    return JsonResponse({
        "total": total,
        "low": IntelligenceArticle.objects.filter(priority="LOW").count(),
        "medium": IntelligenceArticle.objects.filter(priority="MEDIUM").count(),
        "high": IntelligenceArticle.objects.filter(priority="HIGH").count(),
        "critical": IntelligenceArticle.objects.filter(priority="CRITICAL").count(),
    })
def threat_radar_page(request):
    articles = IntelligenceArticle.objects.filter(
        priority__in=["HIGH", "CRITICAL"]
    ).order_by("-id")[:300]

    return render(request, "analytics/threat_radar.html", {
        "articles": articles
    })