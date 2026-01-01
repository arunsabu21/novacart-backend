import resend
from django.conf import settings
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created


from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    # just log for now — NO EMAIL SENDING
    reset_url = f"https://example.com/reset-password/{reset_password_token.user.pk}/{reset_password_token.key}"
    print("RESET URL:", reset_url)
    return


