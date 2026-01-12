from django.urls import path
from .views import add_to_cart, get_cart, remove_from_cart, update_quantity, bulk_delete_cart, bulk_move_to_wishlist

urlpatterns = [
    path("add/", add_to_cart),
    path("", get_cart),
    path("remove/<int:cart_id>/", remove_from_cart),
    path("update/<int:cart_id>/", update_quantity),
    path("bulk-delete/", bulk_delete_cart),
    path("bulk-move-to-wishlist/", bulk_move_to_wishlist),
]