from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import LostItem, Category
from .forms import LostItemForm


# -----------------------
# HOME PAGE
# -----------------------
def home(request):
    latest_items = LostItem.objects.order_by("-created_at")[:6]
    return render(request, "core/home.html", {"latest_items": latest_items})


# -----------------------
# ITEM LIST (with search + category filter)
# -----------------------
def item_list(request):
    query = request.GET.get("q", "")
    selected_category = request.GET.get("category", "")

    categories = Category.objects.all()
    items = LostItem.objects.all()

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if selected_category:
        items = items.filter(category_id=selected_category)

    return render(
        request,
        "core/item_list.html",
        {
            "items": items,
            "categories": categories,
            "query": query,
            "selected_category": selected_category,
        },
    )


# -----------------------
# ITEM DETAIL
# -----------------------
def item_detail(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    return render(request, "core/item_detail.html", {"item": item})


# -----------------------
# CREATE ITEM (upload form)
# -----------------------
@login_required
def item_create(request):
    if request.method == "POST":
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect("item_detail", pk=item.pk)
    else:
        form = LostItemForm()

    return render(request, "core/item_form.html", {"form": form})


# -----------------------
# MARK ITEM AS CLAIMED
# -----------------------
@login_required
@require_POST
def mark_claimed(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    item.status = "CLAIMED"
    item.save()
    return redirect("item_detail", pk=pk)


# -----------------------
# CUSTOM 404
# -----------------------
def custom_404(request, exception):
    return render(request, "core/404.html", status=404)


# -----------------------
# CUSTOM 500
# -----------------------
def custom_500(request):
    return render(request, "core/500.html", status=500)
