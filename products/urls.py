from django.urls import path
from .views import BookListCreateView, BookDetailView, WishlistView, BrandListView, PriceRangeView

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list'),
    path("brands/", BrandListView.as_view()),
    path("price-range/", PriceRangeView.as_view(), name="price-range"),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path("wishlist/", WishlistView.as_view()),
    path("wishlist/<int:pk>/", WishlistView.as_view()),
]
