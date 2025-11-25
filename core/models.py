from django.db import models
from django.contrib.auth.models import User

class ItemCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class LostItem(models.Model):
    STATUS_CHOICES = (
        ('FOUND', 'Found'),
        ('CLAIMED', 'Claimed'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(ItemCategory, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    location_found = models.CharField(max_length=100)
    date_found = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='FOUND')
    created_at = models.DateTimeField(auto_now_add=True)
    found_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
