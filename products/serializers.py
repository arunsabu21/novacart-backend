from rest_framework import serializers
from .models import Book, Wishlist


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "book", "book_id", "created_at"]
