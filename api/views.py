from django.http import JsonResponse

from intelligence.models import (
    IntelligenceArticle,
    Country,
    NewsSource
)


def dashboard_stats(request):

    total_articles = IntelligenceArticle.objects.count()

    high_priority = IntelligenceArticle.objects.filter(
        priority="HIGH"
    ).count()

    critical_priority = IntelligenceArticle.objects.filter(
        priority="CRITICAL"
    ).count()

    total_countries = Country.objects.count()

    total_sources = NewsSource.objects.count()

    data = {
        "metrics": {
            "total_intel": total_articles,
            "high_priority": high_priority,
            "critical_alerts": critical_priority,
            "countries_count": total_countries,
            "active_sources": total_sources,
        }
    }

    return JsonResponse(data)
from intelligence.models import IntelligenceArticle


def intelligence_feed(request):

    country = request.GET.get("country")
    priority = request.GET.get("priority")

    articles = IntelligenceArticle.objects.all().order_by("-published_date")

    if country:
        articles = articles.filter(country__name__icontains=country)

    if priority:
        articles = articles.filter(priority=priority)

    data = []

    for article in articles[:100]:

        data.append({
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "country": article.country.name if article.country else "",
            "priority": article.priority,
            "threat_score": article.threat_score,
            "published": article.published_date.strftime("%d-%m-%Y %H:%M")
        })

    return JsonResponse({
        "articles": data
    })
from intelligence.models import Country


def country_stats(request):

    data = []

    countries = Country.objects.all()

    for country in countries:

        article_count = (
            IntelligenceArticle.objects
            .filter(country=country)
            .count()
        )

        threat_avg = (
            IntelligenceArticle.objects
            .filter(country=country)
        )

        score = 0

        if threat_avg.exists():

            total = 0

            for item in threat_avg:
                total += item.threat_score

            score = int(
                total /
                threat_avg.count()
            )

        data.append({

            "country": country.name,

            "articles": article_count,

            "threat_score": score

        })

    return JsonResponse(
        {"countries": data}
    )
from django.http import JsonResponse
from intelligence.models import Country, IntelligenceArticle


def country_stats(request):

    countries = Country.objects.all()

    output = []

    for country in countries:

        articles = IntelligenceArticle.objects.filter(
            country=country
        )

        article_count = articles.count()

        score = 0

        if article_count > 0:

            total = 0

            for article in articles:
                total += article.threat_score

            score = int(total / article_count)

        output.append({

            "country": country.name,

            "articles": article_count,

            "threat_score": score

        })

    return JsonResponse({

        "countries": output

    })

from django.http import JsonResponse
from intelligence.models import IntelligenceArticle


def get_name(obj):
    if not obj:
        return ""

    if hasattr(obj, "name"):
        return obj.name

    return str(obj)


def intelligence_feed(request):
    qs = IntelligenceArticle.objects.all().order_by("-id")[:300]

    data = []

    for a in qs:
        data.append({
            "id": a.id,
            "title": a.title,
            "summary": a.summary,
            "country": get_name(a.country),
            "category": get_name(a.category),
            "source": get_name(a.source),
            "priority": a.priority,
            "threat_score": a.threat_score,
            "source_url": a.source_url,
            "image_url": a.image_url,
            "video_url": a.video_url,
            "published": str(a.published_date) if a.published_date else "",
        })

    return JsonResponse({
        "articles": data
    })
from django.http import JsonResponse
from intelligence.models import IntelligenceArticle

def country_news(request):

    country=request.GET.get("country","")

    articles=IntelligenceArticle.objects.filter(
        country__icontains=country
    ).order_by('-id')[:50]

    data=[]

    for a in articles:

        data.append({

            "title":a.title,
            "summary":a.summary,
            "source":a.source,
            "priority":a.priority

        })

    return JsonResponse({

        "country":country,
        "articles":data

    })
from intelligence.models import IntelligenceArticle
from django.http import JsonResponse

def country_news(request):

    country=request.GET.get(
        "country",
        ""
    )

    qs=IntelligenceArticle.objects.filter(
        country__icontains=country
    ).order_by('-id')[:50]

    data=[]

    for a in qs:

        data.append({

            "title":a.title,

            "summary":a.summary,

            "source":a.source

        })

    return JsonResponse({

        "articles":data

    })
from django.http import JsonResponse
from intelligence.models import IntelligenceArticle


def ai_prediction(request):
    country = request.GET.get("country", "")
    question = request.GET.get("q", "")

    articles = IntelligenceArticle.objects.filter(
        country__name__icontains=country
    ).order_by("-id")[:20]

    if not articles.exists():
        return JsonResponse({
            "answer": "No latest intelligence available for this country."
        })

    high = articles.filter(priority="HIGH").count()
    critical = articles.filter(priority="CRITICAL").count()
    medium = articles.filter(priority="MEDIUM").count()

    keywords = []

    for a in articles:
        text = (a.title + " " + a.summary).lower()

        if "war" in text or "border" in text:
            keywords.append("border/military tension")
        if "cyber" in text:
            keywords.append("cyber activity")
        if "drone" in text:
            keywords.append("drone threat")
        if "missile" in text:
            keywords.append("missile activity")
        if "terror" in text:
            keywords.append("terror threat")
        if "protest" in text:
            keywords.append("internal unrest")

    keywords = list(set(keywords))

    risk = "LOW"
    if critical > 0:
        risk = "CRITICAL"
    elif high >= 2:
        risk = "HIGH"
    elif medium >= 2:
        risk = "MEDIUM"

    prediction = f"""
    <b>AI Prediction for {country}</b><br><br>
    Current Risk Level: <b>{risk}</b><br>
    Latest Articles Analyzed: <b>{articles.count()}</b><br>
    Critical Alerts: <b>{critical}</b><br>
    High Alerts: <b>{high}</b><br><br>
    <b>Likely Developments:</b><br>
    """

    if keywords:
        prediction += "Possible focus areas: " + ", ".join(keywords) + ".<br><br>"
    else:
        prediction += "No major threat keyword detected. Situation appears routine.<br><br>"

    prediction += """
    <b>AI Recommendation:</b><br>
    Continue monitoring latest alerts, verify source reliability, and track related developments for next 24-48 hours.
    """

    return JsonResponse({
        "answer": prediction
    })
from django.http import JsonResponse
from intelligence.models import IntelligenceArticle

def priority_stats(request):

    return JsonResponse({
        "LOW": IntelligenceArticle.objects.filter(priority="LOW").count(),
        "MEDIUM": IntelligenceArticle.objects.filter(priority="MEDIUM").count(),
        "HIGH": IntelligenceArticle.objects.filter(priority="HIGH").count(),
        "CRITICAL": IntelligenceArticle.objects.filter(priority="CRITICAL").count(),
    })
def latest_alerts(request):
    qs = IntelligenceArticle.objects.filter(
        priority__in=["HIGH", "CRITICAL"]
    ).order_by("-id")[:20]

    data = []

    for a in qs:
        data.append({
            "id": a.id,
            "title": a.title,
            "summary": a.summary,
            "country": a.country.name if a.country else "Global",
            "source": a.source.name if a.source else "Unknown",
            "priority": a.priority,
            "threat_score": a.threat_score,
            "source_url": a.source_url,
            "image_url": a.image_url,
            "published": str(a.published_date) if a.published_date else "",
        })

    return JsonResponse({
        "alerts": data
    })
from django.http import JsonResponse
from intelligence.models import IntelligenceArticle


def get_name(obj):
    if not obj:
        return "Global"

    if hasattr(obj, "name"):
        return obj.name

    return str(obj)


def ai_prediction(request):
    country = request.GET.get("country", "")
    question = request.GET.get("q", "")

    if not country:
        return JsonResponse({
            "answer": "Please select a country first."
        })

    qs = IntelligenceArticle.objects.all().order_by("-id")

    articles = [
        a for a in qs
        if get_name(a.country).lower() == country.lower()
    ][:30]

    if not articles:
        return JsonResponse({
            "answer": f"No latest intelligence available for {country}."
        })

    critical = len([a for a in articles if a.priority == "CRITICAL"])
    high = len([a for a in articles if a.priority == "HIGH"])
    medium = len([a for a in articles if a.priority == "MEDIUM"])

    risk = "LOW"
    if critical > 0:
        risk = "CRITICAL"
    elif high >= 2:
        risk = "HIGH"
    elif medium >= 2:
        risk = "MEDIUM"

    focus = set()

    for a in articles:
        text = f"{a.title} {a.summary}".lower()

        if "border" in text or "war" in text or "military" in text:
            focus.add("Military / Border Tension")
        if "cyber" in text or "hack" in text:
            focus.add("Cyber Activity")
        if "missile" in text or "drone" in text:
            focus.add("Missile / Drone Threat")
        if "terror" in text or "attack" in text:
            focus.add("Terror / Internal Security")
        if "protest" in text or "election" in text:
            focus.add("Political / Civil Unrest")

    focus_text = ", ".join(focus) if focus else "No major threat pattern detected"

    answer = f"""
    <b>STRATEGIC FORECAST: {country}</b><br><br>

    <b>Current Risk Level:</b> {risk}<br>
    <b>Assessment Window:</b> Next 24–72 hours<br>
    <b>Articles Analyzed:</b> {len(articles)}<br>
    <b>Critical Alerts:</b> {critical} | <b>High Alerts:</b> {high} | <b>Medium Alerts:</b> {medium}<br><br>

    <b>Key Indicators Detected:</b><br>
    {focus_text}<br><br>

    <b>Likely Developments:</b><br>
    1. Increased monitoring requirement around identified threat indicators.<br>
    2. Possible escalation in security, defence, cyber or diplomatic activity if related news volume increases.<br>
    3. Situation may remain unstable if HIGH or CRITICAL alerts continue in the next update cycle.<br><br>

    <b>Operational Impact:</b><br>
    - Watch for military movement, cyber incidents, diplomatic statements and public unrest.<br>
    - Verify latest reports from multiple reliable sources before action.<br><br>

    <b>AI Recommendation:</b><br>
    Maintain close watch for the next 24–72 hours. Prioritize HIGH and CRITICAL items, compare with country-wise trend, and review original source links.
    """

    return JsonResponse({
        "answer": answer
    })
def daily_sitrep(request):
    articles = IntelligenceArticle.objects.all().order_by("-id")[:50]

    total = articles.count()
    critical = articles.filter(priority="CRITICAL").count()
    high = articles.filter(priority="HIGH").count()
    medium = articles.filter(priority="MEDIUM").count()

    top_items = ""
    for i, a in enumerate(articles[:10], start=1):
        country = a.country.name if a.country else "Global"
        top_items += f"{i}. [{a.priority}] {a.title} ({country})<br>"

    risk = "LOW"
    if critical > 0:
        risk = "CRITICAL"
    elif high >= 3:
        risk = "HIGH"
    elif medium >= 5:
        risk = "MEDIUM"

    answer = f"""
    <b>IDIGAS DAILY SITREP</b><br><br>

    <b>Overall Risk Level:</b> {risk}<br>
    <b>Total Articles Reviewed:</b> {total}<br>
    <b>Critical:</b> {critical} | <b>High:</b> {high} | <b>Medium:</b> {medium}<br><br>

    <b>Top Intelligence Items:</b><br>
    {top_items}<br>

    <b>AI Assessment:</b><br>
    Current intelligence flow indicates <b>{risk}</b> level monitoring requirement.
    Priority should be given to HIGH and CRITICAL items, especially cyber, defence,
    border, terrorism, missile, drone and geopolitical indicators.<br><br>

    <b>Recommended Action:</b><br>
    Continue monitoring for the next 24–72 hours and verify major developments from original sources.
    """

    return JsonResponse({"sitrep": answer})
from django.http import JsonResponse
from intelligence.models import IntelligenceArticle


def get_obj_name(obj, default="Global"):
    if not obj:
        return default
    if hasattr(obj, "name"):
        return obj.name
    return str(obj)


def daily_sitrep(request):
    qs = IntelligenceArticle.objects.all().order_by("-id")[:50]
    articles = list(qs)

    total = len(articles)
    critical = len([a for a in articles if a.priority == "CRITICAL"])
    high = len([a for a in articles if a.priority == "HIGH"])
    medium = len([a for a in articles if a.priority == "MEDIUM"])

    risk = "LOW"
    if critical > 0:
        risk = "CRITICAL"
    elif high >= 3:
        risk = "HIGH"
    elif medium >= 5:
        risk = "MEDIUM"

    top_items = ""

    for i, a in enumerate(articles[:10], start=1):
        country = get_obj_name(a.country)
        top_items += f"{i}. [{a.priority}] {a.title} ({country})<br>"

    if not top_items:
        top_items = "No latest intelligence available.<br>"

    sitrep = f"""
    <b>IDIGAS DAILY SITREP</b><br><br>

    <b>Overall Risk Level:</b> {risk}<br>
    <b>Total Articles Reviewed:</b> {total}<br>
    <b>Critical:</b> {critical} | <b>High:</b> {high} | <b>Medium:</b> {medium}<br><br>

    <b>Top Intelligence Items:</b><br>
    {top_items}<br>

    <b>AI Assessment:</b><br>
    Current intelligence flow indicates <b>{risk}</b> level monitoring requirement.
    Priority should be given to HIGH and CRITICAL items, especially cyber, defence,
    border, terrorism, missile, drone and geopolitical indicators.<br><br>

    <b>Recommended Action:</b><br>
    Continue monitoring for the next 24–72 hours and verify major developments from original sources.
    """

    return JsonResponse({
        "sitrep": sitrep
    })