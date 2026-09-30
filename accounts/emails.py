from django.conf import settings
from django.core.mail import send_mail


def send_code_email(user, code, purpose="signup"):
    """Email a verification code. In dev this prints to the console backend."""
    if purpose == "login":
        subject = "Your DK Fashions login code"
        intro = "Use this code to finish signing in to DK Fashions:"
    else:
        subject = "Confirm your DK Fashions account"
        intro = "Welcome to DK Fashions! Use this code to confirm your email:"

    ttl = getattr(settings, "EMAIL_CODE_TTL_MINUTES", 15)
    message = (
        f"Hi {user.display_name},\n\n"
        f"{intro}\n\n"
        f"    {code}\n\n"
        f"This code expires in {ttl} minutes. If you didn't request it, ignore this email.\n\n"
        f"— DK Fashions"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
