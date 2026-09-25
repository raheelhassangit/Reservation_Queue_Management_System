from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        PROVIDER = "provider", "Provider"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)