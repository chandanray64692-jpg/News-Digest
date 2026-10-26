def analyze_article(article):

    text = (
        article.title + " " +
        article.summary
    ).lower()

    sentiment = "NEUTRAL"
    risk = "LOW"

    if any(word in text for word in [
        "war","missile","terror",
        "attack","military"
    ]):
        sentiment = "NEGATIVE"
        risk = "HIGH"

    elif any(word in text for word in [
        "cyber","security","spy",
        "intelligence"
    ]):
        sentiment = "NEGATIVE"
        risk = "MEDIUM"

    tags = []

    if "china" in text:
        tags.append("China")

    if "india" in text:
        tags.append("India")

    if "drone" in text:
        tags.append("Drone")

    if "cyber" in text:
        tags.append("Cyber")

    article.sentiment = sentiment
    article.risk_level = risk
    article.ai_tags = ",".join(tags)

    article.ai_summary = (
        f"AI Assessment: {risk} risk article. "
        f"Sentiment: {sentiment}."
    )

    article.save()