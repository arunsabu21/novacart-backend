from django.urls import path
from .views import address_list_create, address_update_delete

urlpatterns = [
    path("", address_list_create),
    path("<int:address_id>/", address_update_delete),
]