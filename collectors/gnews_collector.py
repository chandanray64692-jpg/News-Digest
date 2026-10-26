import requests

from .news_sources import GNEWS_API_KEY

def fetch_gnews():

    url=(
    "https://gnews.io/api/v4/top-headlines"
    "?lang=en"
    f"&apikey={GNEWS_API_KEY}"
    )

    try:

        r=requests.get(url,timeout=20)

        data=r.json()

        return data.get("articles",[])

    except:

        return []