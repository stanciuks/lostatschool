from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import LostItem, Category


def home(request):
    return redirect("item_list")


class ItemListView(ListView):
    model = LostItem
    template_name = "core/item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        qs = LostItem.objects.all()

        q = self.request.GET.get("q", "")
        if q:
            qs = qs.filter(title__icontains=q)

        category = self.request.GET.get("category", "")
        if category:
            qs = qs.filter(category_id=category)

        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["selected_category"] = self.request.GET.get("category", "")
        ctx["query"] = self.request.GET.get("q", "")
        return ctx


@method_decorator(login_required, name="dispatch")
class ItemCreateView(CreateView):
    model = LostItem
    fields = ["title", "description", "category", "image"]
    template_name = "core/item_form.html"
    success_url = reverse_lazy("item_list")


class ItemDetailView(DetailView):
    model = LostItem
    template_name = "core/item_detail.html"
    context_object_name = "item"


# Custom error pages
def custom_404(request, exception):
    return render(request, "core/404.html", status=404)


def custom_500(request):
    return render(request, "core/500.html", status=500)
