from django.db import models
from django.utils import timezone


def safe_image_path(instance, filename):
    return f"lost_items/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class LostItem(models.Model):
    STATUS_CHOICES = [
        ("FOUND", "Found"),
        ("CLAIMED", "Claimed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=safe_image_path)

    location_found = models.CharField(max_length=200, blank=True, null=True)
    date_found = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="FOUND")

    def __str__(self):
        return self.title
