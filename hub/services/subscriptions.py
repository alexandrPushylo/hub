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

def get_subscription_by_id(subscriptions_id: int) -> Subscriptions | None:
    try:
        subscriptions = Subscriptions.objects.get(id=subscriptions_id)
        return subscriptions
    except Subscriptions.DoesNotExist:
        log.info('Subscription does not exist')
        return None


def get_subscription_to_dict(subscriptions_id: int) -> dict:
    subscription = get_subscription_by_id(subscriptions_id)
    return {
        'id': subscription.id,
        'logo': subscription.logo,
        'title': subscription.title,
        'category': subscription.category,
        'start_of_subscription': subscription.start_of_subscription,
        'next_payment_date': subscription.next_payment_date,
        'paid_period': subscription.paid_period,
        'notification_period': subscription.notification_period,
        'amount': subscription.amount,
        'currency': subscription.currency,
        'total_paid_for': subscription.total_paid_for,
        'link': subscription.link,
        'comment': subscription.comment,
        'date_of_creation': subscription.date_of_creation,
    }


def get_active_subscriptions():
    subscriptions = Subscriptions.objects.filter(
        is_active=True,
    ).select_related('category')
    out = []
    for subscription in subscriptions:
        out.append(
            {
                'id': subscription.id,
                'logo': subscription.logo,
                'title': subscription.title,
                'category': subscription.category,
                'start_of_subscription': subscription.start_of_subscription,
                'next_payment_date': subscription.next_payment_date,
                'paid_period': subscription.paid_period,
                'notification_period': subscription.notification_period,
                'amount': subscription.amount,
                'currency': subscription.currency,
                'total_paid_for': subscription.total_paid_for,
                'link': subscription.link,
                'comment': subscription.comment,
                'date_of_creation': subscription.date_of_creation,
            }
        )
    return out

def deactivate_subscription(subscription_id: int) -> Subscriptions | None:
    subscription = get_subscription_by_id(subscription_id)
    if subscription:
        subscription.is_active = False
        subscription.save(update_fields=['is_active'])
        return subscription
    else:
        return None

