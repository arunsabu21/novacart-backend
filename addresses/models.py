from django.conf import settings
from django.db import models


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses"
    )
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)
    address = models.TextField()
    is_default = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.pincode}"
