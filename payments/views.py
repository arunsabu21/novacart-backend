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
import logging

logger = logging.getLogger(__name__)
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

    total_amount = sum(item.quantity * item.product.price for item in cart_items)

    with transaction.atomic():
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
    payment, created = Payment.objects.update_or_create(
        order=order,
        defaults={
            "stripe_payment_intent": intent.id,
            "amount": total_amount,
            "status": "CREATED",
        },
    )

    logger.info(f"Saved UPI: {payment.stripe_payment_intent}")

    return Response(
        {
            "client_secret": intent.client_secret,
            "amount": total_amount,
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    logger.info(f"Webhook hit. Signature present: {bool(sig_header)}")

    # ✅ Verify signature
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError:
        logger.error("❌ Invalid signature")
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"❌ Webhook error: {str(e)}")
        return HttpResponse(status=400)

    event_type = event["type"]
    logger.info(f"🔥 EVENT RECEIVED: {event_type}")

    # Always ACK early
    response = HttpResponse(status=200)

    # ===============================
    # ✅ PAYMENT SUCCESS
    # ===============================
    if event_type == "payment_intent.succeeded":
        logger.info("✅ PAYMENT SUCCESS HANDLER TRIGGERED")
        handle_payment_intent_succeeded(event)
        return response

    # ===============================
    # ✅ REFUND EVENTS (FIXED)
    # ===============================
    if "refund" in event_type:
        logger.info("REFUND EVENT RECEIVED")

        data = event["data"]["object"]
        payment_intent = data.get("payment_intent")

        if not payment_intent:
            charge_obj = data.get("charge")

            if isinstance(charge_obj, dict):
                payment_intent = charge_obj.get("payment_intent")
            elif isinstance(charge_obj, str):
                try:
                    charge = stripe.Charge.retrieve(charge_obj)
                    payment_intent = charge.payment_intent
                except Exception as e:
                    logger.error(f"CHARGE FETCH FAILED: {str(e)}")
                    logger.error("Continuing without payment_intent")
        if not payment_intent:
            logger.warning("STILL NO PAYMENT INTENT")
            return response

        payment = Payment.objects.filter(stripe_payment_intent=payment_intent).first()

        if not payment:
            logger.warning(f"PAYMENT NOT FOUND: {payment_intent}")
            return response
        if payment.status == "REFUNDED":
            logger.info("ALREADY REFUNDED")
            return response

        payment.status = "REFUNDED"
        payment.save(update_fields=["status"])

        order = payment.order

        for item in order.items.all():
            if item.status in ["REFUND_REQUESTED", "CANCELLED"]:
                item.status = "REFUNDED"
                item.save(update_fields=["status"])

        order.status = "REFUNDED"
        order.save(update_fields=["status"])
        logger.info(f"Order {order.id} marked REFUNDED")
        return response

    # ===============================
    # 🔁 IGNORE OTHER EVENTS
    # ===============================
    logger.info(f"ℹ️ Ignored event: {event_type}")
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
            logger.info(f"Order Found: {order_id}, {order.status}")

            cart_items = Cart.objects.filter(user=order.user)
            logger.info(f"CART COUNT: {cart_items.count()}")

            if not cart_items.exists():
                return

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.price,
                    status="CONFIRMED",
                )

            cart_items.delete()

            order.status = "CONFIRMED"
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

        if order.status != "CONFIRMED":
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
