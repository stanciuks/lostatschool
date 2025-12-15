"""Database models for the lost-and-found application."""

import os
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone


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
        Category,
        on_delete=models.PROTECT,
        related_name="items",
    )

    image = models.ImageField(
        upload_to=safe_image_path,
        blank=True,
        null=True,
    )

    location_found = models.CharField(max_length=200, blank=True)
    date_found = models.DateField(default=timezone.now)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="FOUND",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="found_items",
    )

    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="claimed_items",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ItemReport(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("reviewed", "Reviewed"),
        ("dismissed", "Dismissed"),
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
        default="new",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


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
        return f"Lost: {self.title}"
