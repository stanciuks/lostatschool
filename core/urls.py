from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/new/', views.item_create, name='item_create'),
    path('items/<int:pk>/claim/', views.item_claim, name='item_claim'),
]
