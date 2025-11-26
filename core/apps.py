from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        from .models import ItemCategory
        defaults = ["Clothing", "Electronics", "Keys", "Bottles", "Accessories", "Other"]
        for name in defaults:
            ItemCategory.objects.get_or_create(name=name)
