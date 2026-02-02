from django.contrib import admin
from .models import Book, Wishlist

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "stock", "category")
    list_filter = ("category",)
    search_fields = ("title",)
    
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "created_at")
