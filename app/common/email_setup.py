from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.schema.authentication import SignupResponseSchema

app = FastAPI()

# Sendgrid Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME="apikey",
    MAIL_PASSWORD="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",
    MAIL_FROM="ma@kpentagdigital.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.sendgrid.net",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS = True
)


def send_email_notif(verification_id, background_tasks, subject, content, email):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=content,
        subtype="plain"
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return SignupResponseSchema(status=True, email_sent=True, verification_id=verification_id, message="Email sent successfully")
