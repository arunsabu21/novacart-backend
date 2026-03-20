from rest_framework import serializers
from .models import Order, OrderItem
from .utils import get_estimated_delivery
from addresses.serializers import AddressSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_subtitle = serializers.CharField(source="product.subtitle", read_only=True)
    product_image = serializers.SerializerMethodField()
    payment_method = serializers.CharField(source="order.payment_method", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_title",
            "product_subtitle",
            "product_image",
            "quantity",
            "status",
            "price_at_purchase",
            "payment_method",
            "cancelled_at",
        ]
        
    def get_product_image(self, obj):
        request = self.context.get("request")
        
        if obj.product and obj.product.image:
            if request:
                return request.build_absolute_uri(obj.product.image.url)
            return obj.product.image.url
        return None


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
