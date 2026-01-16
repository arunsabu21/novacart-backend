from rest_framework import serializers
from .models import Cart
from django.utils import timezone
from orders.utils import get_estimated_delivery


class CartSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_subtitle = serializers.SerializerMethodField()
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )
    product_image = serializers.ImageField(source="product.image", read_only=True)
    total_price = serializers.SerializerMethodField()
    stock = serializers.IntegerField(source="product.stock", read_only=True)
    estimated_delivery = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "product",
            "product_title",
            "product_subtitle",
            "product_price",
            "product_image",
            "quantity",
            "stock",
            "total_price",
            "estimated_delivery",
        ]

    def get_product_subtitle(self, obj):
        return obj.product.subtitle

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

    def get_estimated_delivery(self, obj):
        date = get_estimated_delivery(timezone.now().date())
        return date.strftime("%d %b %y")
