# collectors/news_sources.py

# Global News
GLOBAL_RSS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
]

# Defence & Military
DEFENSE_RSS = [
    "https://www.defensenews.com/arc/outboundfeeds/rss/",
    "https://breakingdefense.com/feed/",
    "https://www.army-technology.com/feed/",
    "https://www.navalnews.com/feed/",
    "https://www.airforce-technology.com/feed/",
]

# Cyber Security
CYBER_RSS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://krebsonsecurity.com/feed/",
    "https://www.bleepingcomputer.com/feed/",
    "https://securityaffairs.com/feed/",
    "https://www.darkreading.com/rss.xml",
]

# Space & Satellite
SPACE_RSS = [
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://spacenews.com/feed/",
]

# India
INDIA_RSS = [
    "https://pib.gov.in/rss.aspx",
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "https://indianexpress.com/section/india/feed/",
    "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
]

# OSINT / Think Tank
OSINT_RSS = [
    "https://www.bellingcat.com/feed/",
    "https://www.longwarjournal.org/feed",
    "https://www.understandingwar.org/rss.xml",
    "https://www.csis.org/rss.xml",
]


# Master Feed List
RSS_FEEDS = (
    GLOBAL_RSS +
    DEFENSE_RSS +
    CYBER_RSS +
    SPACE_RSS +
    INDIA_RSS +
    OSINT_RSS
)

NEWS_API_KEY = ""
GNEWS_API_KEY = ""