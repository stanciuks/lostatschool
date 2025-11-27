from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages

from .models import LostItem, Category
from .forms import LostItemForm


def home(request):
    recent_items = LostItem.objects.filter(status="FOUND").order_by("-created_at")[:6]
    return render(request, "core/home.html", {"recent_items": recent_items})


def item_list(request):
    query = request.GET.get("q", "")
    selected_category = request.GET.get("category", "")

    categories = Category.objects.all()
    items = LostItem.objects.filter(id__isnull=False)

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_found__icontains=query)
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


def item_detail(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    return render(request, "core/item_detail.html", {"item": item})


@login_required
def item_create(request):
    if request.method == "POST":
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.status = "FOUND"
            item.save()
            messages.success(request, "Item added successfully!")
            return redirect("item_detail", pk=item.pk)
    else:
        form = LostItemForm()

    return render(request, "core/item_form.html", {"form": form})


@login_required
@require_POST
def item_claim(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    if not item.is_claimed:
        item.status = "CLAIMED"
        item.save()
        messages.success(request, "Item marked as claimed.")
    else:
        messages.info(request, "This item is already marked as claimed.")
    return redirect("item_detail", pk=pk)
