import os
import re
import requests
import feedparser
from dotenv import load_dotenv

from intelligence.models import IntelligenceArticle
from collectors.news_sources import (
    CYBER_RSS,
    DEFENSE_RSS,
    GLOBAL_RSS,
    INDIA_RSS,
    SPACE_RSS,
    OSINT_RSS,
)

load_dotenv()

NEWS_API_KEY = os.getenv("5e8c1455369a401788a3195d9e28821a", "")

ALL_FEEDS = GLOBAL_RSS + DEFENSE_RSS + CYBER_RSS + SPACE_RSS + INDIA_RSS + OSINT_RSS


COUNTRY_COORDS = {
    "India": [20.5937, 78.9629],
    "Pakistan": [30.3753, 69.3451],
    "China": [35.8617, 104.1954],
    "Russia": [61.5240, 105.3188],
    "Ukraine": [48.3794, 31.1656],
    "United States": [37.0902, -95.7129],
    "Israel": [31.0461, 34.8516],
    "Iran": [32.4279, 53.6880],
    "Afghanistan": [33.9391, 67.7100],
    "Bangladesh": [23.6850, 90.3563],
    "Sri Lanka": [7.8731, 80.7718],
    "Nepal": [28.3949, 84.1240],
    "Myanmar": [21.9162, 95.9560],
    "Japan": [36.2048, 138.2529],
    "Taiwan": [23.6978, 120.9605],
    "France": [46.2276, 2.2137],
    "Germany": [51.1657, 10.4515],
    "United Kingdom": [55.3781, -3.4360],
    "Canada": [56.1304, -106.3468],
    "Australia": [-25.2744, 133.7751],
}


def model_has_field(field_name):
    return any(f.name == field_name for f in IntelligenceArticle._meta.fields)


def detect_country(text):
    text = (text or "").lower()

    for country in COUNTRY_COORDS:
        if country.lower() in text:
            return country

    if "usa" in text or "u.s." in text or "america" in text:
        return "United States"

    return "Global"


def get_priority_and_score(text):
    text = (text or "").lower()

    critical = ["nuclear", "ballistic", "terror attack", "invasion", "state of emergency"]
    high = ["war", "attack", "missile", "terror", "border", "conflict", "military", "airstrike", "drone"]
    medium = ["cyber", "security", "protest", "crime", "election", "sanction", "violence", "spy", "intelligence"]

    if any(w in text for w in critical):
        return "CRITICAL", 95
    if any(w in text for w in high):
        return "HIGH", 80
    if any(w in text for w in medium):
        return "MEDIUM", 50

    return "LOW", 20


def extract_rss_image(item):
    if "media_content" in item:
        try:
            return item.media_content[0].get("url", "")
        except Exception:
            pass

    if "links" in item:
        for link in item.links:
            if link.get("type", "").startswith("image"):
                return link.get("href", "")

    summary = item.get("summary", "")
    match = re.search(r'<img[^>]+src="([^"]+)"', summary)
    if match:
        return match.group(1)

    return ""


def clean_html(text):
    return re.sub("<.*?>", "", text or "").strip()


def save_article(
    title,
    summary,
    source="Unknown",
    source_url="",
    image_url="",
    video_url="",
    country=None,
):
    if not title:
        return False

    if IntelligenceArticle.objects.filter(title=title).exists():
        return False

    full_text = f"{title} {summary}"

    if not country:
        country = detect_country(full_text)

    priority, threat_score = get_priority_and_score(full_text)

    data = {
        "title": title[:500],
        "summary": clean_html(summary),
        "priority": priority,
    }

    if model_has_field("country"):
        data["country"] = country

    if model_has_field("source"):
        data["source"] = source

    if model_has_field("source_url"):
        data["source_url"] = source_url

    if model_has_field("image_url"):
        data["image_url"] = image_url

    if model_has_field("video_url"):
        data["video_url"] = video_url

    if model_has_field("threat_score"):
        data["threat_score"] = threat_score

    if model_has_field("ai_summary"):
        data["ai_summary"] = f"{priority} risk intelligence. AI monitoring recommended."

    IntelligenceArticle.objects.create(**data)
    return True


def collect_all_news():
    imported = 0

    for feed_url in ALL_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            source_name = feed.feed.get("title", "RSS Source")

            for item in feed.entries[:50]:
                title = item.get("title", "")
                summary = item.get("summary", "")
                source_url = item.get("link", "")
                image_url = extract_rss_image(item)

                if save_article(
                    title=title,
                    summary=summary,
                    source=source_name,
                    source_url=source_url,
                    image_url=image_url,
                ):
                    imported += 1

        except Exception as e:
            print("RSS ERROR:", feed_url, e)

    return imported


def fetch_newsapi():
    if not NEWS_API_KEY:
        print("NEWS_API_KEY missing in .env")
        return 0

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": "India OR Pakistan OR China OR Taiwan OR Russia OR Ukraine OR Israel OR Iran OR military OR defence OR cyber OR missile OR drone OR border OR intelligence OR terrorism",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 50,
        "apiKey": NEWS_API_KEY,
    }

    imported = 0

    try:
        response = requests.get(url, params=params, timeout=20)
        data = response.json()

        print("NEWSAPI STATUS:", data.get("status"))
        print("NEWSAPI MESSAGE:", data.get("message", ""))

        for item in data.get("articles", []):
            source = item.get("source", {}).get("name", "NewsAPI")

            if save_article(
                title=item.get("title", ""),
                summary=item.get("description", ""),
                source=source,
                source_url=item.get("url", ""),
                image_url=item.get("urlToImage", ""),
                video_url="",
            ):
                imported += 1

    except Exception as e:
        print("NEWSAPI ERROR:", e)

    return imported


def fetch_country_news(country):
    if not NEWS_API_KEY:
        print("NEWS_API_KEY missing in .env")
        return []

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": country,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": NEWS_API_KEY,
    }

    articles = []

    try:
        response = requests.get(url, params=params, timeout=20)
        data = response.json()

        print("COUNTRY NEWS STATUS:", data.get("status"))
        print("COUNTRY NEWS MESSAGE:", data.get("message", ""))

        for item in data.get("articles", []):
            title = item.get("title", "")
            summary = item.get("description", "")
            source = item.get("source", {}).get("name", "NewsAPI")
            source_url = item.get("url", "")
            image_url = item.get("urlToImage", "")

            priority, threat_score = get_priority_and_score(f"{title} {summary}")

            save_article(
                title=title,
                summary=summary,
                source=source,
                source_url=source_url,
                image_url=image_url,
                country=country,
            )

            articles.append({
                "title": title,
                "summary": summary,
                "source": source,
                "source_url": source_url,
                "image_url": image_url,
                "country": country,
                "priority": priority,
                "threat_score": threat_score,
            })

    except Exception as e:
        print("COUNTRY NEWS ERROR:", e)

    return articles