from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

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

def get_categories() -> [SubscriptionsCategory]:
    categories = SubscriptionsCategory.objects.all().values()
    return categories

def get_subscription_instance(subscription_id: int | None) -> Subscriptions | None:
    if subscription_id:
        return get_subscription_by_id(subscription_id)
    else:
        return Subscriptions()

def set_data(subscription_instance: Subscriptions, data: dict):
    s_i = subscription_instance
    logo_ = data['logo']
    title_ = data['title']
    category_ = int(data['category'])
    # start_of_subscription_ = data['start_of_subscription']
    start_of_subscription_ = datetime.strptime(data['start_of_subscription'], '%Y-%m-%d').date()
    paid_period_ = data['paid_period']
    notification_period_ = data['notification_period']
    amount_ = float(data['amount'])
    currency_ = data['currency']
    link_ = data['link']
    comment_ = data['comment']

    next_payment_date_ = calculate_next_payment_date(
        start_payment_date=start_of_subscription_,
        paid_period=paid_period_,
    )

    total_paid_for_ = calculate_total_paid_for(
        start_payment_date=start_of_subscription_,
        next_payment_date=get_next_payment_date(
            period=paid_period_,
            current_date=start_of_subscription_
        ),
        amount=amount_
    )

    if logo_:
        s_i.logo = f'logos/{s_i.id}/{logo_}'
    s_i.title = title_
    s_i.category_id = category_
    s_i.start_of_subscription = start_of_subscription_
    s_i.next_payment_date = next_payment_date_
    s_i.paid_period = paid_period_
    s_i.notification_period = notification_period_
    s_i.amount = amount_
    s_i.currency = currency_
    s_i.total_paid_for = total_paid_for_
    s_i.link = link_
    s_i.comment = comment_
    s_i.save()


def calculate_total_paid_for(start_payment_date: date, next_payment_date: date, amount: float) -> float:
    diff_day0 = (date.today() - start_payment_date).days
    diff_day1 = (next_payment_date - start_payment_date).days

    if diff_day1 != 0:
        count = round(diff_day0 / diff_day1)
        total_paid_for = amount * count
        return total_paid_for
    else:
        return 0

def calculate_next_payment_date(start_payment_date: date, paid_period: str) -> date:
    next_payment_date = start_payment_date

    while next_payment_date < date.today():
        next_payment_date = get_next_payment_date(paid_period, next_payment_date)
    return next_payment_date


def get_next_payment_date(period: str, current_date: date) -> date:
    match period:
        case PaidPeriod.D1.value:
            return current_date + timedelta(days=1)
        case PaidPeriod.D2.value:
            return current_date + timedelta(days=2)
        case PaidPeriod.W1.value:
            return current_date + timedelta(weeks=1)
        case PaidPeriod.W2.value:
            return current_date + timedelta(weeks=2)
        case PaidPeriod.W3.value:
            return current_date + timedelta(weeks=3)
        case PaidPeriod.M1.value:
            return current_date + relativedelta(months=+1)
        case PaidPeriod.M2.value:
            return current_date + relativedelta(months=+2)
        case PaidPeriod.M3.value:
            return current_date + relativedelta(months=+3)
        case PaidPeriod.M6.value:
            return current_date + relativedelta(months=+6)
        case PaidPeriod.Y1.value:
            return current_date + relativedelta(years=+1)
        case _:
            return current_date