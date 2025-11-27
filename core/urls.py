from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/create/', views.item_create, name='item_create'),
    path('item/<int:pk>/claim/', views.item_claim, name='item_claim'),
]
