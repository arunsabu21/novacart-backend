import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    order_id = request.data.get("order_id")

    if not order_id:
        return Response({"error": "Order ID Required"}, status=400)

    order = Order.objects.get(id=order_id, user=request.user)

    intent = stripe.PaymentIntent.create(
        amount=int(order.total_amount * 100),
        currency="inr",
        automatic_payment_methods={
            "enabled": True,
            "allow_redirects": "never",
        },
        metadata={
            "order_id": str(order.id),
        },
    )

    # PAYMENT RECORD
    Payment.objects.update_or_create(
        order=order,
        defaults={
            "stripe_payment_intent": intent.id,
            "amount": order.total_amount,
            "status": "CREATED",
        },
    )

    return Response(
        {"payment_intent_id": intent.id, "client_secret": intent.client_secret}
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")

        if not order_id:
            return HttpResponse(status=400)

        try:
            order = Order.objects.get(id=int(order_id))

            order.status = "PAID"
            order.save()

            Payment.objects.update_or_create(
                order=order,
                defaults={
                    "stripe_payment_intent": intent["id"],
                    "amount": intent["amount"] / 100,
                    "status": "SUCCEEDED",
                },
            )

        except Exception as e:
            return HttpResponse(status=500)

    return HttpResponse(status=200)


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
