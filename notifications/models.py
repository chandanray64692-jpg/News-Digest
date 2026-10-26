from django.db import models

class Notification(models.Model):

    TYPES=[
        ("INFO","INFO"),
        ("WARNING","WARNING"),
        ("SUCCESS","SUCCESS"),
        ("CRITICAL","CRITICAL")
    ]

    title=models.CharField(max_length=200)
    message=models.TextField()
    type=models.CharField(max_length=20,choices=TYPES,default="INFO")

    is_read=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title