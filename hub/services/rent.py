from django.db.models import QuerySet

from hub.models import Rent
from hub.utilites import TODAY, get_prev_month, MONTH

from logger import getLogger

log = getLogger(__name__)


def get_rent_by_id(bills_id):
    if bills_id is None:
        rent = Rent.objects.filter(payment_month=get_prev_month(), payment_date__month=MONTH)
        if rent.exists():
            return rent.last()
    try:
        return Rent.objects.get(id=bills_id)
    except Rent.DoesNotExist:
        return None


def get_last_rent() -> Rent:
    rent = Rent.objects.filter().order_by('payment_date').last()
    return rent

def get_prev_rent() -> Rent | None:
    last_rent = get_last_rent()
    if last_rent is None:
        return None
    rent = Rent.objects.filter(payment_date__lt=last_rent.payment_date).first()
    return rent

def get_data_rent(rent: Rent) -> dict:
    out = {}
    out = get_prev_data_rent(out)
    if rent:
        out['title'] = rent.title
        out['id'] = rent.id
        out['payment_date'] = rent.payment_date
        out['payment_month'] = rent.payment_month
        out['amount'] = str(rent.amount)
    else:
        rent = get_last_rent()
        if rent:
            out['title'] = rent.title
            out['payment_date'] = TODAY()
            out['payment_month'] = get_prev_month()
    return out


def get_prev_data_rent(out: dict):
    prev_rent = get_prev_rent()
    if prev_rent:
        pass
    return out


def set_data_rent(rent: Rent, data: dict) -> bool:
    if not rent:
        rent = Rent()
    try:
        operation = data['operation']
        payment_date = data['payment_date']
        payment_month = data['payment_month']
        amount = data['rent_amount']

        # if not all((rate, indications, volume,)):
        #     return False

        # amount = calculate_rent_amount(rate, volume)

        rent.payment_date = payment_date
        rent.payment_month = payment_month
        rent.amount = amount
        rent.save()
        return True
    except TypeError as e:
        log.error('set_data_rent(): TypeError' + e)
        return False



def get_info_rent() -> list:
    rent = Rent.objects.filter().order_by('-payment_date').values()
    return rent


def delete_rent(rent_id):
    if rent_id:
        try:
            Rent.objects.get(pk=rent_id).delete()
            return True
        except Rent.DoesNotExist:
            return False
