from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "name",
            "mobile",
            "pincode",
            "state",
            "district",
            "town",
            "house_number",
            "address",
            "is_default",
        ]

    def validate_mobile(self, value):
        if not value.isdigit() or len(value) not in [10, 12, 13]:
            raise
        serializers.ValidationError("Invalid Mobile Number")
        return value

    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise
        serializers.ValidationError("Invalid Pincode")
        return value
