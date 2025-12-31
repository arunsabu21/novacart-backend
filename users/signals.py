import resend
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):

    reset_url = f"https://novacart-frontend-url/reset-password/{reset_password_token.user.pk}/{reset_password_token.key}"

    resend.Emails.send(
        {
            "from": "NovaCart <onboarding@resend.dev>",
            "to": reset_password_token.email,
            "subject": "Reset your NovaCart password",
            "html": f"""
        <h2>Password Reset</h2>
        <p>Click the link below to reset your password.</p>
        <a href="{reset_url}">{reset_url}</a>
        """,
        }
    )
