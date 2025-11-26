from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
import os
import imghdr


# ==============================
# IMAGE VALIDATION
# ==============================

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
MAX_FILE_SIZE_MB = 5


def validate_file_extension(file):
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError("Only JPG, JPEG, PNG, and WEBP images are allowed.")


def validate_file_size(file):
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File size cannot exceed {MAX_FILE_SIZE_MB}MB.")


def validate_real_image(file):
    # Check real file type (not just extension)
    file_type = imghdr.what(file)
    if file_type not in ALLOWED_EXTENSIONS:
        raise ValidationError("Uploaded file is not a valid image.")


# ==============================
# RANDOM FILE NAME
# ==============================

def random_image_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("item_images", new_filename)


# ==============================
# CATEGORY MODEL
# ==============================

class ItemCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==============================
# LOST ITEM MODEL
# ==============================

class LostItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )

    location_found = models.CharField(max_length=100)
    date_found = models.DateField()

    image = models.ImageField(
        upload_to=random_image_path,
        validators=[validate_file_extension, validate_file_size, validate_real_image],
        blank=True,
        null=True,
    )

    found_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="found_items"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.location_found})"
