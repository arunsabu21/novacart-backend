from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.CharField(max_length=255)
    published_year = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to="books/", null=True, blank=True)  # 🔥 added
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="wishlisted_books")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'book')
        
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
