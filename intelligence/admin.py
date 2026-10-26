from django.contrib import admin
from .models import *

admin.site.register(Country)
admin.site.register(Category)
admin.site.register(NewsSource)
admin.site.register(IntelligenceArticle)