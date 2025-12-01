"""Application configuration for the core app."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Core app configuration for the lost-and-found system."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
