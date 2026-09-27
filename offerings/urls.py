from django.urls import path
from .views import OfferingCreateView

urlpatterns = [
    path("", OfferingCreateView.as_view(), name="offering-create"),
]