import uuid
import os
from django.db import models
from django.utils import timezone


# -----------------------------
#  Generate safe unique filenames
# -----------------------------
def safe_image_path(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"{uuid.uuid4()}.{ext}"
    return os.path.join("items/", new_name)


# -----------------------------
#  Category Model
# -----------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# -----------------------------
#  Lost Item Model
# -----------------------------
class LostItem(models.Model):
    STATUS_CHOICES = [
        ("FOUND", "Found"),
        ("CLAIMED", "Claimed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=safe_image_path, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="FOUND")

    date_found = models.DateTimeField(default=timezone.now)

    def is_recent(self):
        return (timezone.now() - self.date_found).days < 3

    def __str__(self):
        return self.title
