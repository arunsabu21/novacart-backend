from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from .models import Order, OrderItem
from addresses.models import Address
from .serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from .utils import get_estimated_delivery
from django.utils import timezone
from django.db import transaction


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        address_id = request.data.get("address_id")
        payment_method = request.data.get("payment_method", "COD")

        if not address_id:
            return Response(
                {"error": "Address is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return Response(
                {"error": "Invalid address"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response(
                {"detail": "Cart is Empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_amount = sum(
            item.quantity * item.product.price for item in cart_items
        )

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                address=address,
                payment_method=payment_method,
                status="CONFIRMED" if payment_method == "COD" else "PENDING",
                total_amount=total_amount,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.price,
                )

            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)

        if order.status == "PAID":
            return Response({"error": "Paid orders cannot be cancelled"}, status=400)

        order.status = "CANCELLED"
        order.save()
        return Response({"message": "Order cancelled"})
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def delivery_estimate_preview(request):
    estimated = get_estimated_delivery(timezone.now().date())
    return Response({"estimated_delivery": estimated})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def latest_order(request):
    order = Order.objects.filter(user=request.user).order_by("-created_at").first()

    if not order:
        return Response({"error": "No orders found"}, status=404)
    serializer = OrderSerializer(order)
    return Response(serializer.data)
