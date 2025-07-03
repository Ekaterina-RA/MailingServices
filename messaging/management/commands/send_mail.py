from django.core.management.base import BaseCommand
from django.utils import timezone
from . models import Mailing


class Command(BaseCommand):
    help = 'Send scheduled mailings'

    def handle(self, *args, **options):
        now = timezone.now()

        # Получаем рассылки, которые нужно отправить
        mailings = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status__in=['created', 'started']
        )

        for mailing in mailings:
            mailing.status = 'started'
            mailing.save()
            send_mailing(mailing)

            # Если время рассылки истекло, помечаем как завершенную
            if mailing.end_time <= now:
                mailing.status = 'completed'
                mailing.save()