from django.core.management.base import BaseCommand
from django.utils import timezone
from mailing.models import Mailing
from mailing.services import send_mailing


class Command(BaseCommand):
    help = 'Process scheduled mailings'

    def handle(self, *args, **options):
        now = timezone.now()
        mailings = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status__in=['created', 'started']
        )

        for mailing in mailings:
            self.stdout.write(f"Processing mailing #{mailing.id}")

            # Обновляем статус рассылки
            mailing.status = 'started'
            mailing.save()

            # Отправляем рассылку
            send_mailing(mailing)

            # Проверяем, не завершилась ли рассылка
            if mailing.end_time <= now:
                mailing.status = 'completed'
                mailing.save()
                self.stdout.write(f"Mailing #{mailing.id} completed")

        self.stdout.write(self.style.SUCCESS('Finished processing mailings'))