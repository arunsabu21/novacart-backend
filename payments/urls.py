from django.urls import path
from .views import create_payment_intent, stripe_webhook


urlpatterns = [
    path("payment-intent/", create_payment_intent),
    path("webhook/", stripe_webhook),
]