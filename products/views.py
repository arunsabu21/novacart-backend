from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book, Wishlist
from cart.models import Cart
from .serializers import BookSerializer, WishlistSerializer


class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.all()
        category = self.request.query_params.get("category")

        if category:
            queryset = queryset.filter(category__slug=category)

        return queryset



class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlists, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            Wishlist.objects.get_or_create(
                user=request.user, book_id=serializer.validated_data["book_id"]
            )
            return Response(
                {"message": "Added to wishlist"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        Wishlist.objects.filter(user=request.user, pk=pk).delete()
        return Response({"message": "Removed from wishlist"})
