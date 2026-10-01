from django.urls import path
from .views import OfferingListCreateView, OfferingDetailView, MyOfferingsView, ArchiveOfferingView

urlpatterns = [
    path("", OfferingListCreateView.as_view(), name="offering-list-create"),
    path("<int:pk>/", OfferingDetailView.as_view(), name="offering-detail"),
    path("mine/", MyOfferingsView.as_view(), name="offering-mine"),
    path("<int:pk>/archive/", ArchiveOfferingView.as_view(), name="offering-archive"),
]