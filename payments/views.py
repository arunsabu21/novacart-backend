import stripe
from django.conf import settings
from django.http import HttpResponse
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from orders.models import Order, OrderItem
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    user = request.user
    address_id = request.data.get("address_id")

    if not address_id:
        return Response({"error": "Address required"}, status=400)

    cart_items = Cart.objects.filter(user=user)
    if not cart_items.exists():
        return Response({"error": "Cart empty"}, status=400)

    total_amount = sum(
        item.quantity * item.product.price for item in cart_items
    )

    order = Order.objects.create(
        user=user,
        address_id=address_id,
        payment_method="ONLINE",
        status="PENDING",
        total_amount=total_amount,
    )

    intent = stripe.PaymentIntent.create(
        amount=int(total_amount * 100),  # paise
        currency="inr",
        automatic_payment_methods={"enabled": True},
        metadata={"order_id": str(order.id)},
    )

    Payment.objects.create(
        order=order,
        stripe_payment_intent=intent.id,
        amount=total_amount,
        status="CREATED",
    )

    return Response({
        "client_secret": intent.client_secret,
        "amount": total_amount,
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    print("Signature Present", bool(sig_header))

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    except Exception:
        return HttpResponse(status=400)

    # ✅ ACK STRIPE IMMEDIATELY
    response = HttpResponse(status=200)

    if event["type"] == "payment_intent.succeeded":
        print("PAYMENT SUCCEEDED AND EVENT RECEIVED")
        handle_payment_intent_succeeded(event)

    return response


def handle_payment_intent_succeeded(event):
    intent = event["data"]["object"]
    order_id = intent["metadata"].get("order_id")

    if not order_id:
        return

    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().get(
                id=int(order_id),
                status="PENDING",
            )
            print("Order Found:", order.id, order.status)

            cart_items = Cart.objects.filter(user=order.user)
            print("CART COUNT:", cart_items.count())

            if not cart_items.exists():
                return

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.price,
                )

            cart_items.delete()
            

            order.status = "PAID"
            order.save(update_fields=["status"])

            Payment.objects.update_or_create(
                order=order,
                defaults={
                    "stripe_payment_intent": intent["id"],
                    "amount": intent["amount"] / 100,
                    "status": "SUCCEEDED",
                },
            )
            

    except Order.DoesNotExist:
        # already processed → ignore
        return


class RefundOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if order.status != "PAID":
            return Response({"error": "Only paid orders can be refunded"}, status=400)

        try:
            payment = order.payment
        except Payment.DoesNotExist:
            return Response({"error": "Payment record missing"}, status=400)

        # Stripe Refund
        stripe.Refund.create(payment_intent=payment.stripe_payment_intent)

        payment.status = "REFUNDED"
        payment.save()

        order.status = "REFUNDED"
        order.save()

        return Response({"message": "Refund Successful"})
