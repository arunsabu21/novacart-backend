from django.conf import settings
from django.db import models


class Address(models.Model):
    HOME = "HOME"
    OFFICE = "OFFICE"

    ADDRESS_TYPE_CHOICES = [
        (HOME, "Home"),
        (OFFICE, "Office"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)

    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    town = models.CharField(max_length=100)

    house_number = models.CharField(max_length=100)
    address = models.TextField()

    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES,
        default=HOME,
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.address_type} - {self.pincode}"
