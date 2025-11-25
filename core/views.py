from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LostItem, ItemCategory
from .forms import LostItemForm
from django.db.models import Q

def home(request):
    recent_items = LostItem.objects.order_by('-created_at')[:6]
    return render(request, 'core/home.html', {'recent_items': recent_items})

def item_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    items = LostItem.objects.all().order_by('-created_at')
    categories = ItemCategory.objects.all()

    if query:
        items = items.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if category_id:
        items = items.filter(category_id=category_id)

    context = {
        'items': items,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    }
    return render(request, 'core/item_list.html', context)

def item_detail(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    return render(request, 'core/item_detail.html', {'item': item})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.found_by = request.user
            item.save()
            return redirect('item_detail', pk=item.pk)
    else:
        form = LostItemForm()
    return render(request, 'core/item_form.html', {'form': form})

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def item_claim(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    item.status = 'CLAIMED'
    item.save()
    return redirect('item_detail', pk=pk)
