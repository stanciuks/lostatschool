from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # item list (now a class-based view)
    path('items/', views.ItemListView.as_view(), name='item_list'),

    # item detail
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),

    # create new item
    path('item/create/', views.ItemCreateView.as_view(), name='item_create'),
]
