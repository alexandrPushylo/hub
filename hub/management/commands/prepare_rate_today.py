from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        from hub.services.exchange_rate import check_currency_data
        check_currency_data()



