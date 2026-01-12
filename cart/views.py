from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart
from products.models import Book, Wishlist
from .serializers import CartSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    book_id = request.data.get("book_id")

    if not book_id:
        return Response({"error": "book_id required"}, status=400)

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    cart_item = Cart.objects.filter(user=request.user, product=book).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(user=request.user, product=book, quantity=1)

    Wishlist.objects.filter(user=request.user, book=book).delete()

    return Response({"message": "Added to cart"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, cart_id):
    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from cart"})
    except Cart.DoesNotExist:
        return Response({"message": "Item not found"}, status=404)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_quantity(request, cart_id):
    action = request.data.get("action")

    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
    except Cart.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()

    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            return Response({"message": "Item Removed from cart"})
    else:
        return Response({"error": "Invalid action"}, status=400)

    return Response({"message": "Quantity Updated"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bulk_delete_cart(request):
    cart_ids = request.data.get("cart_ids", [])

    if not cart_ids:
        return Response(
            {"error": "cart_ids is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    deleted, _ = Cart.objects.filter(
        id__in=cart_ids,
        user=request.user,
    ).delete()

    return Response(
        {"message": f"{deleted} items removed from bag"}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bulk_move_to_wishlist(request):
    cart_ids = request.data.get("cart_ids", [])

    if not cart_ids:
        return Response(
            {"error": "cart_ids required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart_items = Cart.objects.filter(
        id__in=cart_ids,
        user=request.user,
    ).select_related("product")

    if not cart_items.exists():
        return Response(
            {"error": "No valid cart items"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    moved = 0
    skipped = 0

    for item in cart_items:
        _, created = Wishlist.objects.get_or_create(
            user=request.user,
            book=item.product,
        )
        if created:
            moved += 1
        else:
            skipped += 1

    # delete AFTER loop
    cart_items.delete()

    return Response(
        {
            "added_to_wishlist": moved,
            "already_in_wishlist": skipped,
            "message": f"{moved} added, {skipped} already existed",
        },
        status=status.HTTP_200_OK,
    )
