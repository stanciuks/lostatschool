from django import forms
from .models import LostItem
from .models import ItemReport



class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = [
            "title",
            "description",
            "category",
            "location_found",
            "date_found",
            "image",
        ]
        widgets = {
            "date_found": forms.DateInput(attrs={"type": "date"}),
        }

class ItemReportForm(forms.ModelForm):
    class Meta:
        model = ItemReport
        fields = ["reason"]
