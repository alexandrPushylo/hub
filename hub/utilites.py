from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

import requests
from django.core.exceptions import ObjectDoesNotExist

from hub.models import Rent, Water, Electricity
# from hub.models import Debt, Debtor, ExchangeRate


from hub.services import water_supply as WATER_S
from hub.services import electricity as ELECTRICITY_S
from hub.services import rent as RENT_S
from hub.services import exchange_rate as EXCHANGE_RATE_S
from hub.services import weather as WEATHER_S
from hub.services import subscriptions as SUB_S

import hub.assets as A

from logger import getLogger
log = getLogger(__name__)

TODAY = date.today
NOW = datetime.now().time
MONTH = datetime.now().month


def get_data_json(url: str) -> dict:
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.ConnectTimeout as e:
        log.error(e)
        return {}
    except requests.exceptions.HTTPError as e:
        log.error(e)
        return {}
    except requests.exceptions.RequestException as e:
        log.error(e)
        return {}
    except Exception as e:
        log.error(e)
        return {}


def get_ru_month(month_eng: str) -> str:
    for month in A.MONTH_CHOICES:
        if month[0] == month_eng:
            return month[1]

def get_prev_month() -> str:
    return A.MONTH_CHOICES[MONTH-2][0]


def get_current_bill(
        bill_id: int | None,
        bill_type: A.Type[Rent | Water | Electricity]
) -> Rent | Water | Electricity | None:
    if bill_id is None:
        item_bill = bill_type.objects.filter(payment_month=get_prev_month(), payment_date__month=MONTH)
        if item_bill.exists():
            return item_bill[0]
    return get_bill_by_id(bill_id, bill_type)

def get_bill_by_id(
        bill_id: int | None,
        bill_type: A.Type[Rent | Water | Electricity]
) -> Rent | Water | Electricity | None:
    try:
        return bill_type.objects.get(id=bill_id)
    except ObjectDoesNotExist:
        log.info('get_bill_by_id(): Bill not found [ObjectDoesNotExist]')
        return None

def get_last_bill(
        bill_type: A.Type[Rent | Water | Electricity]
) -> Rent | Water | Electricity | None:
    last_bill = bill_type.objects.filter().order_by('-payment_date')
    return last_bill[0] if last_bill.exists() else None

def get_prev_bill(
        bill_type: A.Type[Rent | Water | Electricity],
        **kwargs
) -> Rent | Water | Electricity | None:
    last_bill = get_last_bill(bill_type)
    if last_bill:
        if kwargs.get('bill_id'):
            prev_bill = bill_type.objects.filter(payment_date__lt=last_bill.payment_date)
            return prev_bill[0] if prev_bill.exists() else None
        else:
            return last_bill
    else:
        return None

def get_data_bill(
        bill_instance: Rent | Water | Electricity,
        **kwargs
) -> dict[str, str]:
    data = {}
    if isinstance(bill_instance, Rent):
        data.update(RENT_S.get_data(bill_instance))
        data.update(RENT_S.get_prev_data(get_prev_bill(Rent, **kwargs)))

    elif isinstance(bill_instance, Water):
        data.update(WATER_S.get_data(bill_instance))
        data.update(WATER_S.get_prev_data(get_prev_bill(Water, **kwargs)))

    elif isinstance(bill_instance, Electricity):
        data.update(ELECTRICITY_S.get_data(bill_instance))
        data.update(ELECTRICITY_S.get_prev_data(get_prev_bill(Electricity, **kwargs)))
    return data

def get_data_last_bill(
        bill_type: A.Type[Rent | Water | Electricity]
) -> dict[str, str] | None:
    last_bill = get_last_bill(bill_type)
    return get_data_bill(last_bill)

def delete_bill(
        bill_id: int,
        bill_type: A.Type[Rent | Water | Electricity]
) -> bool:
    bill = get_bill_by_id(bill_id, bill_type)
    if bill:
        bill.delete()
        log.info('bill was deleted')
        return True
    else:
        log.info('bill was not deleted')
        return False

def get_list_bill(
        bill_type: A.Type[Rent | Water | Electricity]
) -> list:
    return bill_type.objects.filter().order_by('-payment_date').values()

def get_data_for_edit_view(
        bill_id: int,
        bill_type: A.Type[Rent | Water | Electricity]
) -> dict:
    if bill_id:
        bill = get_bill_by_id(bill_id, bill_type)
    else:
        bill = get_last_bill(bill_type)
    data = get_data_bill(bill, bill_id=bill_id)
    return data

def get_bill_type(type_of_bill:str) -> A.Type[Rent | Water | Electricity] | None:
    match type_of_bill:
        case A.Bills.WATER_SUPPLY.value:
            return Water
        case A.Bills.ELECTRICITY.value:
            return Electricity
        case A.Bills.RENT.value:
            return Rent
        case _:
            return None


def set_data_bill(
        bill_instance: Rent | Water | Electricity,
        data: dict[str, str]
) -> bool:
    status = A.Status.ERROR.value
    if isinstance(bill_instance, Rent):
        if RENT_S.set_data(bill_instance, data):
            status = A.Status.OK.value

    elif isinstance(bill_instance, Water):
        if WATER_S.set_data(bill_instance, data):
            status = A.Status.OK.value

    elif isinstance(bill_instance, Electricity):
        if ELECTRICITY_S.set_data(bill_instance, data):
            status = A.Status.OK.value

    return status


def get_inform_data() -> dict:
    data = {
        'today': TODAY(),
        'weather': WEATHER_S.get_main_indicators(get_weather())
    }
    return data

def get_weather():
    data = get_data_json(WEATHER_S.URL)
    return data

def get_current_currency_data() -> dict:
    return EXCHANGE_RATE_S.check_currency_data()

# ====================================================================================================================

def get_subs_by_id(subscription_id: int) -> SUB_S.Subscriptions | None:
    return SUB_S.get_subscription_by_id(subscription_id)

def get_subs_to_dict(subscription_id: int) -> dict:
    return SUB_S.get_subscription_to_dict(subscription_id)

def get_str_notification(notification_period: str) -> str:
    for item in A.NOTIFICATION_PERIOD_CHOICES:
        if item[0] == notification_period:
            return item[1]

def get_str_paid_period(paid_period: str) -> str:
    for item in A.PAID_PERIOD_CHOICES:
        if item[0] == paid_period:
            return f'Каждые {item[1]}'


def get_str_next_payment_date(next_payment_period: date) -> str:
    date_diff = relativedelta(next_payment_period, TODAY())

    if date_diff.years != 0:
        if date_diff.years == 1:
            return f'Через {date_diff.years} год'
        elif date_diff.years in (2, 3, 4,):
            return f'Через {date_diff.years} года'
        else:
            return f'Через {date_diff.years} лет'

    elif date_diff.months != 0:
        if date_diff.months == 1:
            return f'Через {date_diff.months} месяц'
        elif date_diff.months in (2, 3, 4,):
            return f'Через {date_diff.months} месяца'
        else:
            return f'Через {date_diff.months} месяцев'

    elif date_diff.weeks != 0:
        if date_diff.weeks == 1:
            return f'Через {date_diff.weeks} неделю'
        elif date_diff.weeks in (2, 3, 4,):
            return f'Через {date_diff.weeks} недели'
        else:
            return f'Через {date_diff.weeks} недель'

    elif date_diff.days != 0:
        if date_diff.days == 1:
            return f'Через {date_diff.days} день'
        elif date_diff.days in (2, 3, 4,):
            return f'Через {date_diff.days} дня'
        else:
            return f'Через {date_diff.days} дней'
    else:
        return ''

def get_subscriptions_value() -> list:
    subscriptions = SUB_S.get_active_subscriptions()
    for subscription in subscriptions:
        subscription['next_payment'] = get_str_next_payment_date(subscription['next_payment_date'])
    return subscriptions


def set_data_subscription(subscription_id: int, data: dict, files: dict):
    mode = A.EditMode.EDIT if subscription_id else A.EditMode.ADD
    SUB_S.set_data(subscription_id, data, files, mode=mode)

