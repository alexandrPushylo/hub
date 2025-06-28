from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        from hub.services.subscriptions import update_next_notification_date
        update_next_notification_date()



