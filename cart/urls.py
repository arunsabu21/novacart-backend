from django.urls import path
from .views import add_to_cart, get_cart, remove_from_cart, update_quantity

urlpatterns = [
    path("add/", add_to_cart),
    path("", get_cart),
    path("remove/<int:cart_id>/", remove_from_cart),
    path("update/<int:cart_id>/", update_quantity)
]