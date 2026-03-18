from django.urls import path
from .views import (
    CreateOrderView,
    MyOrdersView,
    cancel_order,
    delivery_estimate_preview,
    latest_order,
    cancel_item_details,
)

urlpatterns = [
    path("create/", CreateOrderView.as_view()),
    path("my/", MyOrdersView.as_view()),
    path("latest/", latest_order),
    path("cancel/<int:order_id>/", cancel_order),
    path("cancel-item/", cancel_item_details),
    path("delivery-estimate/", delivery_estimate_preview),
]
