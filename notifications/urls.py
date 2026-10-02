from django.urls import path
from .views import NotificationListView, MarkReadView
urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("<int:pk>/read/", MarkReadView.as_view(), name="notification-read"),
]