from django.core.mail import send_mail
from django.conf import settings
from mailing.models import MailingAttempt


def send_mailing(mailing):
    """Функция для отправки рассылки"""
    clients = mailing.clients.all()
    message = mailing.message

    for client in clients:
        try:
            send_mail(
                subject=message.subject,
                message=message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False,
            )
            # Записываем успешную попытку
            MailingAttempt.objects.create(
                mailing=mailing,
                status="success",
                server_response="Email sent successfully",
            )
        except Exception as e:
            # Записываем неудачную попытку
            MailingAttempt.objects.create(
                mailing=mailing, status="failed", server_response=str(e)
            )
