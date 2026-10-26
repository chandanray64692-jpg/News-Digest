from django.db import models

class Alert(models.Model):

    LEVELS=[
    ("INFO","INFO"),
    ("WARNING","WARNING"),
    ("CRITICAL","CRITICAL")
    ]

    title=models.CharField(max_length=300)

    message=models.TextField()

    level=models.CharField(
    max_length=20,
    choices=LEVELS,
    default="INFO"
    )

    active=models.BooleanField(default=True)

    created_at=models.DateTimeField(
    auto_now_add=True
    )

    def __str__(self):
        return self.title