from django.urls import path
from .views import OfferingListCreateView, OfferingDetailView

urlpatterns = [
    path("", OfferingListCreateView.as_view(), name="offering-list-create"),
    path("<int:pk>/", OfferingDetailView.as_view(), name="offering-detail"),
]