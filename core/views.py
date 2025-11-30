from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import LostItem, Category, ItemReport
from .forms import LostItemForm, ItemReportForm



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
    items = (
        LostItem.objects.all()
        .select_related("category")
        .order_by("-date_found")
    )

    # GET parameters
    q = request.GET.get("q", "").strip()
    category_id = request.GET.get("category") or ""
    status = request.GET.get("status") or ""
    order = request.GET.get("order") or "newest"

    # Search by keywords
    if q:
        items = items.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(location_found__icontains=q)
        )

    # Category filter
    if category_id:
        items = items.filter(category_id=category_id)

    # Status filter
    if status == "unclaimed":
        items = items.filter(is_claimed=False)
    elif status == "claimed":
        items = items.filter(is_claimed=True)

    # Sorting
    if order == "oldest":
        items = items.order_by("date_found")
    else:
        items = items.order_by("-date_found")

    # Pagination
    paginator = Paginator(items, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all().order_by("name")

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "q": q,
        "current_category": category_id,
        "current_status": status,
        "current_order": order,
    }
    return render(request, "core/item_list.html", context)



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
        form = ItemReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.item = item
            report.reported_by = request.user
            report.save()
            return redirect("item_detail", pk=pk)

    else:
        form = ItemReportForm()

    return render(request, "core/report_item.html", {"form": form, "item": item})



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

@login_required
def dashboard(request):
    my_reports = (
        ItemReport.objects.filter(reported_by=request.user)
        .select_related("item")
        .order_by("-created_at")
    )

    # Unclaimed = status = "FOUND"
    recent_unclaimed = (
        LostItem.objects.filter(status="FOUND")
        .order_by("-date_found")[:5]
    )

    # Claimed = status = "CLAIMED"
    recent_claimed = (
        LostItem.objects.filter(status="CLAIMED")
        .order_by("-date_found")[:5]
    )

    context = {
        "my_reports": my_reports,
        "recent_unclaimed": recent_unclaimed,
        "recent_claimed": recent_claimed,
    }

    return render(request, "core/dashboard.html", context)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def report_center(request):
    status_filter = request.GET.get("status", "")

    reports = ItemReport.objects.select_related("item", "reported_by")

    if status_filter in ["new", "reviewed", "dismissed"]:
        reports = reports.filter(status=status_filter)

    reports = reports.order_by("-created_at")

    context = {
        "reports": reports,
        "current_status": status_filter,
    }

    return render(request, "core/report_center.html", context)

@staff_member_required
def set_report_status(request, pk, new_status):
    report = get_object_or_404(ItemReport, pk=pk)

    if new_status not in ["new", "reviewed", "dismissed"]:
        return redirect("report_center")

    report.status = new_status
    report.save()

    return redirect("report_center")
