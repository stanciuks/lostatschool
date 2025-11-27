from django.db import models
from django.utils import timezone
import os
from uuid import uuid4
from django.conf import settings


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
        max_length=20,
        choices=STATUS_CHOICES,
        default="FOUND"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_claimed(self):
        return self.status == "CLAIMED"


# ✅ FIXED: ItemReport must NOT be inside LostItem
class ItemReport(models.Model):
    STATUS_NEW = "new"
    STATUS_REVIEWED = "reviewed"
    STATUS_DISMISSED = "dismissed"

    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_DISMISSED, "Dismissed"),
    ]

    item = models.ForeignKey(
        LostItem,
        on_delete=models.CASCADE,
        related_name="reports",
    )
    reason = models.TextField()
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="item_reports",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report for {self.item.title} ({self.created_at:%Y-%m-%d})"
