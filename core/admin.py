"""Admin configuration for the core application."""
from django.contrib import admin

from .models import Category, LostItem

admin.site.register(Category)
admin.site.register(LostItem)

