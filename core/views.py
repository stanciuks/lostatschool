from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q

from .models import LostItem, ItemCategory
from .forms import LostItemForm


# ========================================
# HOME PAGE (LIST + SEARCH + CATEGORY)
# ========================================

def home(request):
    query = request.GET.get("q", "")
    selected_category = request.GET.get("category", "")

    items = LostItem.objects.all()
    categories = ItemCategory.objects.all()

    # Text search
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_found__icontains=query)
        )

    # Category filter
    if selected_category:
        items = items.filter(category_id=selected_category)

    context = {
        "items": items,
        "categories": categories,
        "query": query,
        "selected_category": selected_category,
    }
    return render(request, "core/item_list.html", context)


# ========================================
# ITEM DETAIL PAGE
# ========================================

def item_detail(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    return render(request, "core/item_detail.html", {"item": item})


# ========================================
# CREATE NEW LOST ITEM
# ========================================

@login_required
def item_create(request):
    if request.method == "POST":
        form = LostItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.found_by = request.user
            item.save()
            return redirect("item_detail", pk=item.pk)
        else:
            print("FORM ERRORS:", form.errors)  # useful debug output

    else:
        form = LostItemForm()

    return render(request, "core/item_form.html", {"form": form})


# ========================================
# CUSTOM ERROR PAGES
# ========================================

def custom_404(request, exception):
    return render(request, "core/404.html", status=404)


def custom_500(request):
    return render(request, "core/500.html", status=500)
