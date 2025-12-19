from django.urls import path
from .views import CreateOrderView, MyOrdersView, cancel_order

urlpatterns = [
    path("create/", CreateOrderView.as_view()),
    path("my/", MyOrdersView.as_view()),
    path("cancel/<int:order_id>/", cancel_order),
]