from django.db import models
from orders.models import Order


class Payment(models.Model):
    STATUS_CHOICES = (
        ("CREATED", "Created"),
        ("SUCCEEDED", "Succeeded"),
        ("FAILED", "Failed"),
    )

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    stripe_payment_intent = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CREATED")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
