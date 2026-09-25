from django.urls import path
from .views import CustomerRegisterView, ProviderRegisterView

urlpatterns = [
    path("register/customer/", CustomerRegisterView.as_view(), name="customer-register"),
    path("register/provider/", ProviderRegisterView.as_view(), name="provider-register"),
]