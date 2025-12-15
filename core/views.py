from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import LostItemForm, ItemReportForm, LostRequestForm
from .models import Category, ItemReport, LostItem, LostRequest


# -------------------------------------------------------------------
# HOME
# -------------------------------------------------------------------
def home(request):
    recent_items = LostItem.objects.order_by("-created_at")[:6]
    return render(request, "core/home.html", {"recent_items": recent_items})


# -------------------------------------------------------------------
# ITEM LIST
# -------------------------------------------------------------------
def item_list(request):
    items = LostItem.objects.select_related("category")

    q = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    status = request.GET.get("status", "")
    order = request.GET.get("order", "newest")

    if q:
        items = items.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(location_found__icontains=q)
        )

    if category_id:
        items = items.filter(category_id=category_id)

    if status == "unclaimed":
        items = items.filter(status="FOUND")
    elif status == "claimed":
        items = items.filter(status="CLAIMED")

    items = items.order_by("date_found" if order == "oldest" else "-date_found")

    paginator = Paginator(items, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "core/item_list.html",
        {
            "page_obj": page_obj,
            "categories": Category.objects.all(),
            "q": q,
            "current_category": category_id,
            "current_status": status,
            "current_order": order,
        },
    )


# -------------------------------------------------------------------
# ITEM DETAIL
# -------------------------------------------------------------------
def item_detail(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    return render(request, "core/item_detail.html", {"item": item})


# -------------------------------------------------------------------
# CREATE ITEM
# -------------------------------------------------------------------
@login_required
def item_create(request):
    if request.method == "POST":
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("item_detail", pk=item.pk)
    else:
        form = LostItemForm()

    return render(request, "core/item_form.html", {"form": form})


# -------------------------------------------------------------------
# EDIT ITEM
# -------------------------------------------------------------------
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

    return render(request, "core/item_edit.html", {"form": form, "item": item})


# -------------------------------------------------------------------
# DELETE ITEM
# -------------------------------------------------------------------
@login_required
def item_delete(request, pk):
    item = get_object_or_404(LostItem, pk=pk)

    if request.method == "POST":
        item.delete()
        return redirect("item_list")

    return render(request, "core/item_delete.html", {"item": item})


# -------------------------------------------------------------------
# MARK AS CLAIMED
# -------------------------------------------------------------------
@login_required
@require_POST
def mark_claimed(request, pk):
    item = get_object_or_404(LostItem, pk=pk)

    if item.status != "CLAIMED":
        item.status = "CLAIMED"
        item.claimed_by = request.user
        item.save()

    return redirect("item_detail", pk=pk)


# -------------------------------------------------------------------
# REPORT ITEM
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------------------
@login_required
def dashboard(request):
    return render(
        request,
        "core/dashboard.html",
        {
            "my_found_items": LostItem.objects.filter(created_by=request.user),
            "my_lost_requests": LostRequest.objects.filter(created_by=request.user),
            "my_reports": ItemReport.objects.filter(reported_by=request.user),
        },
    )


# -------------------------------------------------------------------
# LOST REQUESTS
# -------------------------------------------------------------------
@login_required
def lost_request_list(request):
    return render(
        request,
        "core/lost_request_list.html",
        {"requests": LostRequest.objects.all()},
    )


@login_required
def lost_request_detail(request, pk):
    lost_request = get_object_or_404(LostRequest, pk=pk)
    return render(
        request,
        "core/lost_request_detail.html",
        {"lost_request": lost_request},
    )


@login_required
def lost_request_create(request):
    if request.method == "POST":
        form = LostRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.created_by = request.user
            req.save()
            return redirect("lost_request_detail", pk=req.pk)
    else:
        form = LostRequestForm()

    return render(request, "core/lost_request_form.html", {"form": form})


@login_required
def lost_request_edit(request, pk):
    lost_request = get_object_or_404(LostRequest, pk=pk)

    if lost_request.created_by != request.user and not request.user.is_staff:
        return redirect("lost_request_detail", pk=pk)

    if request.method == "POST":
        form = LostRequestForm(request.POST, instance=lost_request)
        if form.is_valid():
            form.save()
            return redirect("lost_request_detail", pk=pk)
    else:
        form = LostRequestForm(instance=lost_request)

    return render(
        request,
        "core/lost_request_form.html",
        {"form": form, "lost_request": lost_request},
    )


@login_required
def lost_request_delete(request, pk):
    lost_request = get_object_or_404(LostRequest, pk=pk)

    if lost_request.created_by != request.user and not request.user.is_staff:
        return redirect("lost_request_detail", pk=pk)

    if request.method == "POST":
        lost_request.delete()
        return redirect("lost_request_list")

    return render(
        request,
        "core/lost_request_delete.html",
        {"lost_request": lost_request},
    )


# -------------------------------------------------------------------
# REPORT CENTER (STAFF)
# -------------------------------------------------------------------
@login_required
@user_passes_test(lambda u: u.is_staff)
def report_center(request):
    reports = ItemReport.objects.select_related(
        "item", "reported_by"
    ).order_by("-created_at")

    return render(
        request,
        "core/report_center.html",
        {"reports": reports},
    )
