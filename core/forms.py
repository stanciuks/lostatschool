"""Forms for the core lost-and-found app."""

from django import forms

from .models import LostItem, ItemReport, LostRequest


class LostItemForm(forms.ModelForm):
    """Form for creating or editing a lost item."""

    class Meta:
        """Meta configuration for LostItemForm."""

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
    """Form for reporting an issue about a lost item."""

    class Meta:
        """Meta configuration for ItemReportForm."""

        model = ItemReport
        fields = ["reason"]
        
class LostRequestForm(forms.ModelForm):
    """Form for users to create a lost-item request."""

    class Meta:
        model = LostRequest
        fields = [
            "title",
            "description",
            "category",
            "location_lost",
            "date_lost",
            "contact_email",
        ]
        widgets = {
            "date_lost": forms.DateInput(attrs={"type": "date"}),
        }

