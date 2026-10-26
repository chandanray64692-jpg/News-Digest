from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, blank=True)
    region = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class NewsSource(models.Model):
    name = models.CharField(max_length=200, unique=True)
    source_type = models.CharField(max_length=30, default="RSS")
    url = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    reliability_score = models.IntegerField(default=50)

    def __str__(self):
        return self.name


class IntelligenceArticle(models.Model):
    PRIORITY = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
        ("CRITICAL", "CRITICAL"),
    ]

    title = models.CharField(max_length=500, unique=True)
    summary = models.TextField(blank=True)
    full_text = models.TextField(blank=True)

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    source = models.ForeignKey(
        NewsSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY,
        default="MEDIUM"
    )

    threat_score = models.IntegerField(default=0)

    sentiment_score = models.FloatField(default=0)

    sentiment = models.CharField(
        max_length=20,
        default="NEUTRAL"
    )

    risk_level = models.CharField(
        max_length=20,
        default="LOW"
    )

    ai_summary = models.TextField(blank=True, null=True)

    ai_tags = models.TextField(blank=True, null=True)

    source_url = models.URLField(blank=True, null=True)

    image_url = models.URLField(blank=True, null=True)

    video_url = models.URLField(blank=True, null=True)

    published_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:80]


class TwitterIntelPost(models.Model):
    PRIORITY = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
        ("CRITICAL", "CRITICAL"),
    ]

    handle = models.CharField(max_length=100)
    author_name = models.CharField(max_length=200, blank=True, null=True)
    post_id = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    post_url = models.URLField(blank=True, null=True)

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY,
        default="LOW"
    )

    category = models.CharField(
        max_length=100,
        default="Twitter OSINT"
    )

    ai_summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(blank=True, null=True)

    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.handle} - {self.priority}"