from rest_framework import serializers
from .models import Book, Wishlist


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        
    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            if request:
                return request.build_absolute_url(obj.image.url)
            return obj.image.url
        return None


class WishlistSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "book", "book_id", "created_at"]
