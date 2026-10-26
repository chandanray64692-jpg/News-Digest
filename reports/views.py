import os
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from intelligence.models import IntelligenceArticle


def get_country_name(country):
    if not country:
        return "Global"

    if hasattr(country, "name"):
        return country.name

    return str(country)


def get_article_date(article):
    if hasattr(article, "published_date") and article.published_date:
        return article.published_date

    if hasattr(article, "created_at") and article.created_at:
        return article.created_at

    return None


def get_threat_score(article):
    score = getattr(article, "threat_score", None)

    if score:
        return score

    priority = str(article.priority).upper()

    if priority == "CRITICAL":
        return 95
    if priority == "HIGH":
        return 80
    if priority == "MEDIUM":
        return 50

    return 20


def get_source(article):
    source = getattr(article, "source", None)

    if not source:
        return "Unknown"

    if hasattr(source, "name"):
        return source.name

    return str(source)


def generate_pdf(request):
    folder = os.path.join(settings.BASE_DIR, "media", "reports")
    os.makedirs(folder, exist_ok=True)

    filename = f"Briefing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(folder, filename)

    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()
    content = []

    content.append(
        Paragraph(
            "IDIGAS Strategic Intelligence Briefing",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    articles = IntelligenceArticle.objects.all().order_by("-id")[:30]

    for article in articles:
        date_value = get_article_date(article)

        content.append(
            Paragraph(
                f"<b>{article.title}</b>",
                styles["Heading3"]
            )
        )

        content.append(
            Paragraph(
                article.summary or "No summary available.",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Priority: {article.priority} | Country: {get_country_name(article.country)} | Source: {get_source(article)}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Threat Score: {get_threat_score(article)} | Published: {date_value if date_value else 'N/A'}",
                styles["BodyText"]
            )
        )

        content.append(Spacer(1, 12))

    doc.build(content)

    return JsonResponse({
        "status": "success",
        "file": filename,
        "path": filepath,
        "url": f"/media/reports/{filename}"
    })


def executive_summary(request):
    articles = IntelligenceArticle.objects.all()

    total = articles.count()
    critical = articles.filter(priority="CRITICAL").count()
    high = articles.filter(priority="HIGH").count()
    medium = articles.filter(priority="MEDIUM").count()
    low = articles.filter(priority="LOW").count()

    countries = set()
    sources = set()
    total_threat = 0

    for article in articles:
        countries.add(get_country_name(article.country))
        sources.add(get_source(article))
        total_threat += int(get_threat_score(article))

    avg_risk = int(total_threat / total) if total else 0

    return JsonResponse({
        "total_articles": total,
        "critical_alerts": critical,
        "high_priority": high,
        "medium_priority": medium,
        "low_priority": low,
        "countries": len(countries),
        "sources": len(sources),
        "average_risk_score": avg_risk,
    })


def sitrep(request):
    latest = []

    articles = IntelligenceArticle.objects.all().order_by("-id")[:20]

    for article in articles:
        date_value = get_article_date(article)

        latest.append({
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "country": get_country_name(article.country),
            "source": get_source(article),
            "priority": article.priority,
            "threat": get_threat_score(article),
            "published": str(date_value) if date_value else "",
            "source_url": getattr(article, "source_url", "") or "",
            "image_url": getattr(article, "image_url", "") or "",
            "video_url": getattr(article, "video_url", "") or "",
        })

    return JsonResponse({
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": latest,
    })


def reports_page(request):
    selected_country = request.GET.get("country", "")
    selected_priority = request.GET.get("priority", "")

    base_articles = IntelligenceArticle.objects.all().order_by("-id")

    country_list = sorted(
        list(
            set(
                [
                    article.country.name
                    for article in base_articles
                    if article.country
                ]
            )
        )
    )

    articles = base_articles

    if selected_country:
        articles = articles.filter(
            country__name__iexact=selected_country
        )

    if selected_priority:
        articles = articles.filter(
            priority=selected_priority
        )

    total = articles.count()
    high = articles.filter(priority="HIGH").count()
    critical = articles.filter(priority="CRITICAL").count()
    medium = articles.filter(priority="MEDIUM").count()
    low = articles.filter(priority="LOW").count()

    risk_total = 0

    for article in articles:
        risk_total += int(get_threat_score(article))

    risk_index = int(risk_total / total) if total else 0

    return render(request, "reports/reports.html", {
        "articles": articles[:300],
        "total": total,
        "high": high,
        "critical": critical,
        "medium": medium,
        "low": low,
        "countries": len(country_list),
        "country_list": country_list,
        "selected_country": selected_country,
        "selected_priority": selected_priority,
        "risk_index": risk_index,
    })


def report_detail(request, article_id):
    article = get_object_or_404(
        IntelligenceArticle,
        id=article_id
    )

    return render(
        request,
        "reports/report_detail.html",
        {
            "article": article,
            "country_name": get_country_name(article.country),
            "source_name": get_source(article),
            "published_value": get_article_date(article),
            "threat_score": get_threat_score(article),
        }
    )