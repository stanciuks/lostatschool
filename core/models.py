"""Database models for the lost-and-found application."""

import os
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone


def safe_image_path(instance, filename):
    """Generate a safe, randomized file path for uploaded images."""
    ext = filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join("items", filename)


class Category(models.Model):
    """Category representing a group of lost items (e.g., clothing, electronics)."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """Meta configuration for Category."""

        ordering = ["name"]

    def __str__(self):
        """Return a human-readable representation of the category."""
        return self.name


class LostItem(models.Model):
    """A single lost item recorded in the system."""

    STATUS_CHOICES = [
        ("FOUND", "Found"),
        ("CLAIMED", "Claimed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="items",
    )
    image = models.ImageField(upload_to=safe_image_path, blank=True, null=True)

    location_found = models.CharField(max_length=200, blank=True)
    date_found = models.DateField(default=timezone.now)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="FOUND",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta configuration for LostItem."""

        ordering = ["-created_at"]

    def __str__(self):
        """Return a human-readable representation of the lost item."""
        return self.title

    @property
    def is_claimed(self):
        """Return True if the item has been claimed."""
        return self.status == "CLAIMED"


class ItemReport(models.Model):
    """A report submitted about a specific lost item."""

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
        """Meta configuration for ItemReport."""

        ordering = ["-created_at"]

    def __str__(self):
        """Return a human-readable representation of the report."""
        return f"Report for {self.item.title} ({self.created_at:%Y-%m-%d})"

class LostRequest(models.Model):
    """A report created by a user when they lose an item."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="lost_requests",
    )

    location_lost = models.CharField(max_length=200, blank=True)
    date_lost = models.DateField(default=timezone.now)

    contact_email = models.EmailField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lost_requests",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Return the lost request title."""
        return f"Lost: {self.title}"
