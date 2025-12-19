from django.urls import path
from .views import create_payment_intent, stripe_webhook, RefundOrderView


urlpatterns = [
    path("payment-intent/", create_payment_intent),
    path("webhook/", stripe_webhook),
    path("refund/<int:order_id>/", RefundOrderView.as_view()),
]