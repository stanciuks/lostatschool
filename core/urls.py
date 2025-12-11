"""URL routes for the core lost-and-found app."""

from django.urls import path

from . import views

urlpatterns = [
    # Public pages
    path("", views.home, name="home"),
    path("items/", views.item_list, name="item_list"),
    path("item/<int:pk>/", views.item_detail, name="item_detail"),

    # CRUD
    path("item/create/", views.item_create, name="item_create"),
    path("item/<int:pk>/edit/", views.item_edit, name="item_edit"),
    path("item/<int:pk>/delete/", views.item_delete, name="item_delete"),

    # Mark item claimed
    path("item/<int:pk>/claimed/", views.mark_claimed, name="mark_claimed"),

    # Reports
    path("item/<int:pk>/report/", views.report_item, name="report_item"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Staff-only reporting center
    path("reports/", views.report_center, name="report_center"),
    path(
        "reports/<int:pk>/set_status/<str:new_status>/",
        views.set_report_status,
        name="set_report_status",
    ),
    path("item/<int:pk>/claim/", views.mark_claimed, name="mark_claimed"),
    path("lost/", views.lost_request_list, name="lost_request_list"),
    path("lost/new/", views.lost_request_create, name="lost_request_create"),

]
