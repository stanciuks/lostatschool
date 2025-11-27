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
    recent_items = LostItem.objects.order_by("-created_at")[:6]
    return render(request, "core/home.html", {"recent_items": recent_items})


# -----------------------
# ITEM LIST
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
# CREATE ITEM
# -----------------------
@login_required
def item_create(request):
    if request.method == "POST":
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            return redirect("item_detail", pk=item.pk)
    else:
        form = LostItemForm()

    return render(request, "core/item_form.html", {"form": form})


# -----------------------
# EDIT ITEM
# -----------------------
@login_required
def item_edit(request, pk):
    item = get_object_or_404(LostItem, pk=pk)

    if request.method == "POST":
        form = LostItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("item_detail", pk=item.pk)
    else:
        form = LostItemForm(instance=item)

    return render(
        request,
        "core/item_edit.html",
        {"form": form, "item": item}
    )



@login_required
def item_delete(request, pk):
    item = get_object_or_404(LostItem, pk=pk)

    if request.method == "POST":
        item.delete()
        return redirect("item_list")

    return render(request, "core/item_delete.html", {"item": item})


from django.core.mail import send_mail
from django.conf import settings

@login_required
def report_item(request, pk):
    item = get_object_or_404(LostItem, pk=pk)

    if request.method == "POST":
        reason = request.POST.get("reason")

        # Send email to admin
        send_mail(
            subject=f"Item Reported: {item.title}",
            message=f"The following item was reported:\n\nTitle: {item.title}\nID: {item.id}\nReason: {reason}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        return redirect("item_detail", pk=item.pk)

    return render(request, "core/report_item.html", {"item": item})


# -----------------------
# MARK AS CLAIMED
# -----------------------
@login_required
@require_POST
def mark_claimed(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    item.status = "CLAIMED"
    item.save()
    return redirect("item_detail", pk=pk)


# -----------------------
# CUSTOM ERROR PAGES
# -----------------------
def custom_404(request, exception):
    return render(request, "core/404.html", status=404)


def custom_500(request):
    return render(request, "core/500.html", status=500)
