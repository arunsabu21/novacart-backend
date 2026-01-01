import resend
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver

# set API key
resend.api_key = settings.RESEND_API_KEY


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):

    # correct frontend link
    reset_url = f"https://novacart-frontend.netlify.app/reset-password/{reset_password_token.user.pk}/{reset_password_token.key}"

    try:
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

        print("RESET EMAIL SENT TO:", reset_password_token.user.email)
        print("RESET URL:", reset_url)

    except Exception as e:
        print("RESEND ERROR:", e)
