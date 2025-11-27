from django import forms
from .models import LostItem

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = [
            "title",
            "description",
            "category",
            "image",
            "location_found",
            "date_found",
        ]
        widgets = {
            "date_found": forms.DateInput(attrs={"type": "date"}),
        }

