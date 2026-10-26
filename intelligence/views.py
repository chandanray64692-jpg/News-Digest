from django.http import JsonResponse
from django.db.models import Q
from intelligence.models import *


def get_country_name(country):
    if not country:
        return ""

    if hasattr(country, "name"):
        return country.name

    return str(country)


def get_category_name(category):
    if not category:
        return ""

    if hasattr(category, "name"):
        return category.name

    return str(category)


def dashboard_stats(request):
    total = IntelligenceArticle.objects.count()
    high = IntelligenceArticle.objects.filter(priority="HIGH").count()
    critical = IntelligenceArticle.objects.filter(priority="CRITICAL").count()

    countries = set()
    sources = set()

    for x in IntelligenceArticle.objects.all():
        if x.country:
            countries.add(get_country_name(x.country))

        if hasattr(x, "source") and x.source:
            sources.add(str(x.source))

        if hasattr(x, "source_url") and x.source_url:
            sources.add(x.source_url)

    return JsonResponse({
        "metrics": {
            "total_intel": total,
            "high_priority": high,
            "critical_alerts": critical,
            "countries_count": len(countries),
            "active_sources": len(sources),
        }
    })


def intelligence_feed(request):
    country = request.GET.get("country", "")
    priority = request.GET.get("priority", "")
    category = request.GET.get("category", "")
    search = request.GET.get("search", "")

    qs = IntelligenceArticle.objects.all()

    if hasattr(IntelligenceArticle, "published_date"):
        qs = qs.order_by("-published_date")
    else:
        qs = qs.order_by("-id")

    if country:
        qs = qs.filter(country__icontains=country)

    if priority:
        qs = qs.filter(priority__iexact=priority)

    if category:
        qs = qs.filter(category__icontains=category)

    if search:
        qs = qs.filter(
            Q(title__icontains=search) |
            Q(summary__icontains=search)
        )

    data = []

    for x in qs[:300]:
        published = ""

        if hasattr(x, "published_date") and x.published_date:
            published = x.published_date.strftime("%d-%m-%Y")

        source = ""

        if hasattr(x, "source") and x.source:
            source = str(x.source)

        if hasattr(x, "source_url") and x.source_url:
            source = x.source_url

        data.append({
            "id": x.id,
            "title": x.title,
            "summary": x.summary,
            "country": get_country_name(x.country),
            "category": get_category_name(getattr(x, "category", "")),
            "priority": x.priority,
            "threat_score": x.threat_score,
            "source": source,
            "published": published,
        })

    return JsonResponse({"articles": data})


def country_stats(request):
    country_data = {}

    for x in IntelligenceArticle.objects.all():
        country = get_country_name(x.country) or "Global"

        if country not in country_data:
            country_data[country] = {
                "count": 0,
                "threat_total": 0
            }

        country_data[country]["count"] += 1
        country_data[country]["threat_total"] += int(x.threat_score or 0)

    output = []

    for country, values in country_data.items():
        count = values["count"]
        threat = int(values["threat_total"] / count) if count else 0

        output.append({
            "country": country,
            "articles": count,
            "threat_score": threat
        })

    return JsonResponse({"countries": output})


def priority_stats(request):
    return JsonResponse({
        "LOW": IntelligenceArticle.objects.filter(priority="LOW").count(),
        "MEDIUM": IntelligenceArticle.objects.filter(priority="MEDIUM").count(),
        "HIGH": IntelligenceArticle.objects.filter(priority="HIGH").count(),
        "CRITICAL": IntelligenceArticle.objects.filter(priority="CRITICAL").count(),
    })


def latest_alerts(request):
    alerts = []

    qs = IntelligenceArticle.objects.filter(
        priority__in=["HIGH", "CRITICAL"]
    ).order_by("-id")[:20]

    for x in qs:
        alerts.append({
            "title": x.title,
            "country": get_country_name(x.country),
            "priority": x.priority,
            "score": x.threat_score
        })

    return JsonResponse({"alerts": alerts})