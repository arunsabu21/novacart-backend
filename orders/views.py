from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from .utils import get_estimated_delivery
from django.utils import timezone


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"detail": "Cart is Empty"}, status=400)

        total_amount = sum(item.quantity * item.product.price for item in cart_items)

        order = Order.objects.create(user=user, total_amount=total_amount)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price,
            )

        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)


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
