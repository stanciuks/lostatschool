"""URL configuration for the core app."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("items/", views.item_list, name="item_list"),
    path("item/<int:pk>/", views.item_detail, name="item_detail"),
    path("item/<int:pk>/edit/", views.item_edit, name="item_edit"),
    path("item/<int:pk>/delete/", views.item_delete, name="item_delete"),
    path("item/create/", views.item_create, name="item_create"),
    path("item/<int:pk>/report/", views.report_item, name="report_item"),
    path("item/<int:pk>/claim/", views.mark_claimed, name="item_claim"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reports/", views.report_center, name="report_center"),
    path(
        "reports/<int:pk>/set_status/<str:new_status>/",
        views.set_report_status,
        name="set_report_status",
    ),
]
