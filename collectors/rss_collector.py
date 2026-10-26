import re
import feedparser
from django.utils import timezone

from intelligence.models import (
    IntelligenceArticle,
    Country,
    Category,
    NewsSource
)

from notifications.models import Notification
from realtime.models import Alert

from ai_engine.services import detect_category, threat_score

from .news_sources import RSS_FEEDS


COUNTRY_KEYWORDS = {
    "India": ["india", "new delhi", "kashmir", "ladakh"],
    "Pakistan": ["pakistan", "islamabad", "karachi"],
    "China": ["china", "beijing", "taiwan", "pla"],
    "Russia": ["russia", "moscow", "kremlin"],
    "Ukraine": ["ukraine", "kyiv"],
    "United States": ["united states", "usa", "america", "washington"],
    "Israel": ["israel", "gaza", "tel aviv"],
    "Iran": ["iran", "tehran"],
    "North Korea": ["north korea", "pyongyang"],
    "Japan": ["japan", "tokyo"],
    "United Kingdom": ["united kingdom", "britain", "london"],
}


def clean_html(text):
    if not text:
        return ""

    text = re.sub(r"<.*?>", "", text)
    return text.strip()


def extract_rss_image(item):
    if hasattr(item, "media_content"):
        try:
            return item.media_content[0].get("url", "")
        except Exception:
            pass

    if hasattr(item, "media_thumbnail"):
        try:
            return item.media_thumbnail[0].get("url", "")
        except Exception:
            pass

    if "links" in item:
        for link in item.links:
            if link.get("type", "").startswith("image"):
                return link.get("href", "")

    summary = item.get("summary", "") or item.get("description", "")

    img = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', summary)

    if img:
        return img.group(1)

    return ""


def detect_country_name(text):
    text = text.lower()

    for country, keywords in COUNTRY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return country

    return "Global"


def get_priority(threat):
    if threat >= 80:
        return "CRITICAL"

    if threat >= 50:
        return "HIGH"

    if threat >= 30:
        return "MEDIUM"

    return "LOW"


def save_article(title, summary, source_url, source_name, image_url=""):
    if not title:
        return False

    if IntelligenceArticle.objects.filter(title=title).exists():
        return False

    full_text = f"{title} {summary}"

    category_name = detect_category(full_text)
    threat = threat_score(full_text)
    priority = get_priority(threat)
    country_name = detect_country_name(full_text)

    category_obj, _ = Category.objects.get_or_create(
        name=category_name or "General"
    )

    country_obj = None

    if country_name != "Global":
        country_obj, _ = Country.objects.get_or_create(
            name=country_name,
            defaults={
                "code": country_name[:3].upper(),
                "region": ""
            }
        )

    source_obj, _ = NewsSource.objects.get_or_create(
        name=source_name or "RSS Source",
        defaults={
            "source_type": "RSS",
            "url": source_url or "",
            "active": True,
            "reliability_score": 60
        }
    )

    article = IntelligenceArticle.objects.create(
        title=title[:500],
        summary=clean_html(summary),
        full_text=clean_html(full_text),
        country=country_obj,
        category=category_obj,
        source=source_obj,
        priority=priority,
        threat_score=threat,
        source_url=source_url,
        image_url=image_url,
        published_date=timezone.now(),
        ai_summary=f"{priority} risk RSS intelligence item. AI review recommended."
    )

    Notification.objects.create(
        title="New Intelligence",
        message=title[:200],
        type="INFO"
    )

    if threat >= 80:
        Alert.objects.create(
            title="Critical Threat",
            message=title[:300],
            level="CRITICAL"
        )

    return True


def collect_rss():
    imported = 0

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            source_name = feed.feed.get("title", "RSS Source")

            for item in feed.entries[:30]:
                title = item.get("title", "")
                summary = item.get("summary", "") or item.get("description", "")
                source_url = item.get("link", "")
                image_url = extract_rss_image(item)

                if save_article(
                    title=title,
                    summary=summary,
                    source_url=source_url,
                    source_name=source_name,
                    image_url=image_url
                ):
                    imported += 1

        except Exception as e:
            print("RSS Error:", feed_url, e)

    return imported