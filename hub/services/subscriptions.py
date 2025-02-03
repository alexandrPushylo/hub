from datetime import date, timedelta

from hub.models import SubscriptionsCategory, Subscriptions
from hub.assets import NOTIFICATION_PERIOD_CHOICES, PAID_PERIOD_CHOICES, CURRENCY_CHOICES
from hub.assets import NotificationPeriod, PaidPeriod, Currency
from logger import getLogger
log = getLogger(__name__)


def get_subscriptions_by_period(period: date):
    subscriptions = Subscriptions.objects.filter(
        next_payment_date__gte=date.today(),
        next_payment_date__lte=period
    )
    return subscriptions