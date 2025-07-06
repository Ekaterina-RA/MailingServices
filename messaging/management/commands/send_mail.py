from django.core.management.base import BaseCommand
from django.utils import timezone
from messaging.models import Mailing, Attempt
from messaging.tasks import send_mailing


class Command(BaseCommand):
    help = 'Send scheduled messages'

    def handle(self, *args, **options):
        now = timezone.now()
        messages = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status=Mailing.CREATED
        )

        for message in messages:
            message.status = Mailing.STARTED
            messages.save()
            send_mailing.delay(message.id)

        self.stdout.write(self.style.SUCCESS(f'Successfully started {messages.count()} messages'))