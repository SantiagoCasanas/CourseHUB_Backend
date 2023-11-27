
from decouple import config
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import ResetPasswordToken

def sendResetPasswordEmail(reset_password_token:ResetPasswordToken):
    forgot_password_token = str(reset_password_token.reset_token)
    user = reset_password_token.user

    greetings = f"Hi {user.username},"
    subject = "Password Reset for COURSEHUB App"
    email_content = f"""
{greetings}

We noticed that you requested a password reset for your COURSEHUB App account.

Please use the following token to reset your password: {forgot_password_token}

If you didn't request this, please ignore this email.

Best regards,
The COURSEHUB Team
"""
    
    try:
        email = EmailMessage(
            subject=subject,
            body=email_content,
            from_email=config('EMAIL_HOST_USER', ''),
            to=[user.email]
        )
        email.fail_silently = True
        email.send()
    except Exception as e:
        return e
