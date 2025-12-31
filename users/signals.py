import resend
from django.conf import settings
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):

    # frontend reset page link
    reset_url = f"http://localhost:5173/reset-password/{reset_password_token.user.pk}/{reset_password_token.key}"

    # set API key
    resend.api_key = settings.RESEND_API_KEY

    resend.Emails.send(
        {
            "from": "NovaCart <onboarding@resend.dev>",
            "to": reset_password_token.user.email,
            "subject": "Reset your NovaCart password",
            "html": f"""
                <h2>Password Reset</h2>
                <p>Click the link below to reset your password:</p>
                <a href="{reset_url}">{reset_url}</a>
            """,
        }
    )
