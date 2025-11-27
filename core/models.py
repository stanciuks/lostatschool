from django.db import models
from django.utils import timezone
import os
from uuid import uuid4


def safe_image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join("items", filename)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class LostItem(models.Model):
    STATUS_CHOICES = [
        ("FOUND", "Found"),
        ("CLAIMED", "Claimed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="items"
    )
    image = models.ImageField(upload_to=safe_image_path, blank=True, null=True)

    location_found = models.CharField(max_length=200, blank=True)
    date_found = models.DateField(default=timezone.now)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="FOUND"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_claimed(self):
        return self.status == "CLAIMED"
