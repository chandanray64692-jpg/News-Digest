from django.shortcuts import render
from intelligence.models import IntelligenceArticle


def alerts_page(request):
    alerts = IntelligenceArticle.objects.filter(
        priority__in=["HIGH", "CRITICAL"]
    ).order_by("-id")[:100]

    return render(request, "notifications/alerts.html", {"alerts": alerts})