from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart
from products.models import Book
from .serializers import CartSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get("book_id")

    if not product_id:
        return Response({"error": "book_id required"}, status=400)

    try:
        product = Book.objects.get(id=product_id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    cart_item = Cart.objects.filter(user=request.user, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(user=request.user, product=product, quantity=1)

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
