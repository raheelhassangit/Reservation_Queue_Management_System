from django.urls import path
from . import views_web

urlpatterns = [
    path("", views_web.offering_list_page, name="offering-list-page"),
    path("dashboard/", views_web.dashboard_page, name="offering-dashboard"),
    path("create/", views_web.offering_create_page, name="offering-create-page"),
    path("<int:pk>/edit/", views_web.offering_edit_page, name="offering-edit-page"),
    path("<int:pk>/", views_web.offering_detail_page, name="offering-detail-page"),
]