from django.urls import path
from .views import BookListCreateView, BookDetailView, WishlistView

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path("wishlist/", WishlistView.as_view()),
    path("wishlist/<int:pk>/", WishlistView.as_view()),
]
