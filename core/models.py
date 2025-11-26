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
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="items/", null=True, blank=True)
    date_found = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="FOUND")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

