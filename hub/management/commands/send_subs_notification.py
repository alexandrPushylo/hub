from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        from hub.utilites import send_subs_notification
        send_subs_notification()



