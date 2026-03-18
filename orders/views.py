from rest_framework.views import APIView
import stripe
from django.conf import settings
from django.db.models import Q
from .pagination import OrderPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from .models import Order, OrderItem
from payments.models import Payment
from addresses.models import Address
from .serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from .utils import get_estimated_delivery
from django.utils import timezone
from django.db import transaction
from .emails import send_order_confirmation_email
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


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

        total_amount = sum(item.quantity * item.product.price for item in cart_items)

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
                    status="CONFIRMED",
                )

            cart_items.delete()
            send_order_confirmation_email(order)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.GET.get("search", "").strip()

        orders = Order.objects.filter(user=request.user).order_by("-created_at")

        if search:
            orders = orders.filter(
                Q(items__product__title__icontains=search)
                | Q(items__product__subtitle__icontains=search)
                | Q(items__product__description__icontains=search)
            ).distinct()

        paginator = OrderPagination()
        paginated_orders = paginator.paginate_queryset(orders, request)

        serializer = OrderSerializer(
            paginated_orders, many=True, context={"request": request}
        )

        return paginator.get_paginated_response(serializer.data)


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


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def cancel_item_details(request):

    if request.method == "GET":
        order_id = request.GET.get("orderId")
        item_id = request.GET.get("itemId")

        try:
            item = OrderItem.objects.select_related("product").get(
                id=item_id, order_id=order_id, order__user=request.user
            )

            return Response(
                {
                    "id": item.id,
                    "product_title": item.product.title,
                    "product_subtitle": item.product.subtitle,
                    "product_image": request.build_absolute_uri(item.product.image.url),
                    "price_at_purchase": item.price_at_purchase,
                    "payment_method": item.order.payment_method,
                }
            )

        except OrderItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

    elif request.method == "POST":
        order_id = request.data.get("orderId")
        item_id = request.data.get("itemId")
        reason = request.data.get("reason")

        try:
            item = OrderItem.objects.get(
                id=item_id, order_id=order_id, order__user=request.user
            )
            # prevent double cancel
            if item.status in ["CANCELLED", "REFUND_REQUESTED"]:
                return Response({"error": "Item already cancelled"}, status=400)

            if item.order.payment_method == "ONLINE":
                item.status = "REFUND_REQUESTED"
            else:
                item.status = "CANCELLED"
            item.save()
            remaining_items = OrderItem.objects.filter(order=item.order).exclude(
                status__in=["CANCELLED", "REFUND_REQUESTED"]
            )

            if not remaining_items.exists():
                if item.order.payment_method == "ONLINE":
                    item.order.status = "REFUND_REQUESTED"
                else:
                    item.order.status = "CANCELLED"
                item.order.save(update_fields=["status"])

            logger.info(
                f"Cancel Request > order:{order_id}, item:{item_id}, user:{request.user}"
            )

            payment = None

            if item.order.payment_method == "ONLINE":
                payment = Payment.objects.filter(order=item.order).first()

            if not payment:
                logger.warning(f"No payment found for order {item.order.id}")

            elif payment.status == "REFUNDED":
                logger.warning(f"Already refunded for order {item.order.id}")

            elif payment.stripe_payment_intent:
                refund_amount = item.price_at_purchase * item.quantity

                payment.status = "REFUND_REQUESTED"
                payment.save(update_fields=["status"])

                try:
                    stripe.Refund.create(
                        payment_intent=payment.stripe_payment_intent,
                        amount=int(refund_amount * 100),
                    )
                except Exception as e:
                    logger.error(f"Stripe refund failed: {str(e)}")
                    return Response({"error": "Refund failed"}, status=500)
                logger.info(f"Refund triggered > amount {refund_amount}")
                return Response({"message": "Item cancelled successfully"})

        except OrderItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def latest_order(request):
    order = Order.objects.filter(user=request.user).order_by("-created_at").first()

    if not order:
        return Response({"error": "No orders found"}, status=404)
    serializer = OrderSerializer(order)
    return Response(serializer.data)
