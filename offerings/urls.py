from django.urls import path
from .views import OfferingListCreateView, OfferingDetailView, MyOfferingsView, ArchiveOfferingView, AddSeatsView

urlpatterns = [
    path("", OfferingListCreateView.as_view(), name="offering-list-create"),
    path("<int:pk>/", OfferingDetailView.as_view(), name="offering-detail"),
    path("mine/", MyOfferingsView.as_view(), name="offering-mine"),
    path("<int:pk>/archive/", ArchiveOfferingView.as_view(), name="offering-archive"),
    path("<int:pk>/add-seats/", AddSeatsView.as_view(), name='add-seats'),
]