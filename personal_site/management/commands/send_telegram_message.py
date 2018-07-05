from django.core.management import BaseCommand

from personal_site.telegram_notifier import send_notification


class Command(BaseCommand):
    help = """Send debug message via the set-up telegram bot"""

    def add_arguments(self, parser):
        parser.add_argument('message',
                            type=str,
                            help='Some text message')

    def handle(self, *args, **kwargs):
        send_notification(text=kwargs['message'])
