import feedparser

from collectors.news_sources import CYBER_RSS, DEFENSE_RSS, GLOBAL_RSS, INDIA_RSS, SPACE_RSS
from intelligence.models import IntelligenceArticle

from collectors.news_sources import RSS_FEEDS

ALL_FEEDS = (
GLOBAL_RSS +
DEFENSE_RSS +
CYBER_RSS +
SPACE_RSS +
INDIA_RSS
)

def collect_all_news():

    imported = 0

    for feed_url in ALL_FEEDS:

        try:

            feed = feedparser.parse(feed_url)

            for item in feed.entries[:50]:

                title = item.get("title","")

                summary = item.get("summary","")

                if IntelligenceArticle.objects.filter(
                    title=title
                ).exists():
                    continue

                IntelligenceArticle.objects.create(

                    title=title,

                    summary=summary

                )

                imported += 1

        except Exception as e:

            print(feed_url,e)

    return imported