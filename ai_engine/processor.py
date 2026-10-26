from intelligence.models import *
from .services import *

def process_article(article):

    text=f"{article.title} {article.summary}"

    article.threat_score=threat_score(text)

    article.save()