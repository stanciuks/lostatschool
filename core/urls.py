from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("items/", views.item_list, name="item_list"),
    path("item/create/", views.item_create, name="item_create"),
    path("item/<int:pk>/", views.item_detail, name="item_detail"),
    path("item/<int:pk>/edit/", views.item_edit, name="item_edit"),
    path("item/<int:pk>/delete/", views.item_delete, name="item_delete"),

    path("item/<int:pk>/claimed/", views.mark_claimed, name="mark_claimed"),
    path("item/<int:pk>/report/", views.report_item, name="report_item"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("lost/", views.lost_request_list, name="lost_request_list"),
    path("lost/new/", views.lost_request_create, name="lost_request_create"),
    path("lost/<int:pk>/", views.lost_request_detail, name="lost_request_detail"),
    path("reports/", views.report_center, name="report_center"),
    path("lost/<int:pk>/edit/", views.lost_request_edit, name="lost_request_edit"),
    path("lost/<int:pk>/delete/", views.lost_request_delete, name="lost_request_delete"),

]