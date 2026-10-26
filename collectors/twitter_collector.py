import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from intelligence.models import TwitterIntelPost

load_dotenv()

X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN", "")
print("X TOKEN FOUND:", bool(X_BEARER_TOKEN))

IMPORTANT_HANDLES = [
    "narendramodi",
    "PMOIndia",
    "DefenceMinIndia",
    "rajnathsingh",
    "adgpi",
    "DRDO_India",
    "isro",
    "WhiteHouse",
    "POTUS",
    "DeptofDefense",
    "NATO",
    "SecDef",
    "IDF",
    "MoD_Russia",
    "ZelenskyyUa",
    "SpaceX",
    "elonmusk",
    "BAESystemsplc",
    "LockheedMartin",
    "BoeingDefense",
    "northropgrumman",
    "RaytheonTech",
]

KEYWORDS_HIGH = [
    "war", "attack", "missile", "drone", "border", "terror",
    "airstrike", "military", "conflict", "nuclear"
]

KEYWORDS_MEDIUM = [
    "cyber", "defence", "defense", "security", "exercise",
    "satellite", "radar", "ai", "technology"
]


def get_headers():
    return {
        "Authorization": f"Bearer {X_BEARER_TOKEN}"
    }


def get_priority(text):
    t = text.lower()

    if any(word in t for word in KEYWORDS_HIGH):
        return "HIGH"

    if any(word in t for word in KEYWORDS_MEDIUM):
        return "MEDIUM"

    return "LOW"


def get_user_id(username):
    url = f"https://api.x.com/2/users/by/username/{username}"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=20
    )

    data = response.json()

    if "data" not in data:
        print("USER ERROR:", username, data)
        return None, None

    return data["data"]["id"], data["data"].get("name", username)


def fetch_user_posts(username, max_results=5):
    user_id, author_name = get_user_id(username)

    if not user_id:
        return 0

    url = f"https://api.x.com/2/users/{user_id}/tweets"

    params = {
        "max_results": max_results,
        "exclude": "replies,retweets",
        "tweet.fields": "created_at,public_metrics,context_annotations"
    }

    response = requests.get(
        url,
        headers=get_headers(),
        params=params,
        timeout=20
    )

    data = response.json()

    if "data" not in data:
        print("POST ERROR:", username, data)
        return 0

    imported = 0

    for post in data["data"]:
        post_id = post["id"]

        if TwitterIntelPost.objects.filter(post_id=post_id).exists():
            continue

        text = post.get("text", "")
        priority = get_priority(text)

        created_at = None
        if post.get("created_at"):
            created_at = datetime.fromisoformat(
                post["created_at"].replace("Z", "+00:00")
            )

        TwitterIntelPost.objects.create(
            handle=username,
            author_name=author_name,
            post_id=post_id,
            text=text,
            post_url=f"https://x.com/{username}/status/{post_id}",
            priority=priority,
            created_at=created_at,
        )

        imported += 1

    return imported


def collect_twitter_intel():
    if not X_BEARER_TOKEN:
        print("X_BEARER_TOKEN missing in .env")
        return 0

    total = 0

    for handle in IMPORTANT_HANDLES:
        try:
            total += fetch_user_posts(handle, max_results=5)
        except Exception as e:
            print("TWITTER ERROR:", handle, e)

    return total