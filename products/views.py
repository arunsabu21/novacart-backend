from rest_framework.decorators import api_view
from django.db.models import Count
from django.db.models import Min, Max
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book, Wishlist
from .serializers import BookSerializer, WishlistSerializer
from django.db.models import Q, F, Case, When, Value
from django.db.models.functions import Substr, StrIndex
from collections import defaultdict


class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.all()

        category = self.request.query_params.get("category")
        brands = self.request.query_params.getlist("brand")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        sort = self.request.query_params.get("sort")

        if category:
            queryset = queryset.filter(category__slug=category)

        if brands:
            queryset = queryset.filter(title__in=brands)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if sort == "price":
            queryset = queryset.order_by("price")

        elif sort == "-price":
            queryset = queryset.order_by("-price")

        return queryset


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BrandListView(APIView):
    def get(self, request):
        category = request.query_params.get("category")

        queryset = Book.objects.all()

        if category:
            queryset = queryset.filter(category__slug=category)

        brands = queryset.values("title").annotate(count=Count("id")).order_by("title")

        return Response(brands)


class PriceRangeView(APIView):
    def get(self, request):
        category = request.query_params.get("category")

        queryset = Book.objects.all()

        if category:
            queryset = queryset.filter(category__slug=category)

        min_price = queryset.aggregate(Min("price"))["price__min"]
        max_price = queryset.aggregate(Max("price"))["price__max"]

        return Response({"min_price": min_price or 0, "max_price": max_price or 0})


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            wishlists, many=True, context={"request": request}
        )
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


@api_view(["GET"])
def auto_suggest(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return Response([])

    categories = (
        Book.objects
        .filter(category__name__icontains=query)
        .values(
            name=F("category__name"),
            slug=F("category__slug"),
            category_image=F("category__image"),
            category_mobile_image=F("category__mobile_image"),
        )
        .annotate(count=Count("id"))
        .order_by("-count")[:5]   
    )

    books = Book.objects.filter(title__icontains=query)

    brand_map = defaultdict(int)

    for book in books:
        if not book.title:
            continue

        brand = book.title.split(" ")[0].strip()
        if brand:
            brand_map[brand] += 1

    brands = sorted(
        [{"name": k, "count": v, "type": "brand"} for k, v in brand_map.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:5]


    results = []

    for c in categories:
        raw_image = c.get("category_mobile_image") or c.get("category_image")
        image_url = (
            request.build_absolute_uri(raw_image)
            if raw_image
            else ""
        )
        results.append({
            "name": c["name"],
            "slug": c["slug"],
            "count": c["count"],
            "image": image_url,
            "type": "category"
        })

    results.extend(brands)

    return Response(results)
