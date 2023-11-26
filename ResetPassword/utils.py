from sendgrid.helpers.mail import Mail
import jwt
from decouple import config
from sendgrid import SendGridAPIClient
from datetime import datetime
from .models import ResetPasswordToken

def sendResetPasswordEmail(reset_password_token:ResetPasswordToken):
    forgot_password_token = str(reset_password_token.reset_token)
    user = reset_password_token.user
    greetings = f"Hola {user.nombre} {user.apellido}," if user.nombre and user.apellido else "Hola"
    email_html_content = f"<html><body><p>{greetings}</p>Por favor, usa este token para CineCritix App:<b> {forgot_password_token}</b></body></html>"

    message = Mail(
        from_email=config('EMAIL_SENDER'),
        to_emails=[user.email],
        subject=f"Recuperar contraseña de CineCritix App. {str(datetime.now())}",
        html_content=email_html_content
    )

    sendgrid_client = SendGridAPIClient(api_key=config('SEND_API'))

    response = sendgrid_client.send(message)

def generate_token(email):
    token = jwt.encode({"email":email}, config('SECRET_KEY'))
    return token