from django.contrib import admin
from .models import Star, Viewing, Observatory, Photo
# Register your models here.
admin.site.register(Star)
admin.site.register(Viewing)
admin.site.register(Observatory)
admin.site.register(Photo)
