from rest_framework import serializers
from .models import Order, OrderItem
from .utils import get_estimated_delivery
from addresses.serializers import AddressSerializer  


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_title",
            "product_image",
            "quantity",
            "price_at_purchase",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)  
    estimated_delivery = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "total_amount",
            "status",
            "created_at",
            "estimated_delivery",
            "address", 
            "items",
        ]

    def get_estimated_delivery(self, obj):
        return get_estimated_delivery(obj.created_at).date()
