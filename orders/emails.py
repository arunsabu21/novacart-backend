from django.template.loader import render_to_string
from django.conf import settings
import resend

resend.api_key = settings.RESEND_API_KEY


def send_order_confirmation_email(order):
    user = order.user
    address = order.address

    items = []
    total_mrp = 0

    for item in order.items.all():
        total_price = item.quantity * item.price_at_purchase
        total_mrp += total_price

        items.append({
            "product_title": item.product.title,  
            "quantity": item.quantity,
            "price": item.price_at_purchase,
            "total_price": total_price,
            "image_url": (
                item.product.image.url
                if item.product.image else ""
            ), 
        })

    context = {
        "user_name": address.name,       
        "order_id": order.id,
        "payment_method": order.payment_method,
        "items": items,
        "total_mrp": total_mrp,
        "total_amount": order.total_amount,
        "address": address,
        "order_url": "https://novacart-frontend.netlify.app/orders",
    }

    html = render_to_string(
        "emails/order_confirmation.html",
        context
    )

    try:
        resend.Emails.send({
            "from": "NovaCart <onboarding@resend.dev>",
            "to": user.email,
            "subject": "Your NovaCart Order is Confirmed 🎉",
            "html": html,
        })
    except Exception as e:
        print("ORDER EMAIL FAILED:", e)