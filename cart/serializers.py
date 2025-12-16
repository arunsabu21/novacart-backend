from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    product_image = serializers.ImageField(source="product.image", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "product",
            "product_title",
            "product_price",
            "product_image",
            "quantity",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity