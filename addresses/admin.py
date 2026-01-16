from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "name",
        "mobile",
        "pincode",
        "state",
        "district",
        "town",
        "is_default",
    )
    list_filter = ("state", "district", "is_default")
    search_fields = ("name", "mobile", "pincode")
