from django.db.models import QuerySet

from hub.models import Electricity
from hub.utilites import TODAY, get_prev_month, MONTH

from logger import getLogger

log = getLogger(__name__)


def get_electricity_by_id(bills_id):
    if bills_id is None:
        electricity = Electricity.objects.filter(payment_month=get_prev_month(), payment_date__month=MONTH)
        if electricity.exists():
            return electricity.last()
    try:
        return Electricity.objects.get(id=bills_id)
    except Electricity.DoesNotExist:
        return None


# def get_water_supply(water_supply_id) -> Water | None:
#     if not water_supply_id:
#         return None
#     try:
#         water_supply = Water.objects.get(id=water_supply_id)
#         return water_supply
#     except Water.DoesNotExist:
#         return None

def get_last_electricity() -> Electricity:
    electricity = Electricity.objects.filter().order_by('payment_date').last()
    return electricity

def get_prev_electricity() -> Electricity | None:
    last_electricity = get_last_electricity()
    if last_electricity is None:
        return None
    electricity = Electricity.objects.filter(payment_date__lt=last_electricity.payment_date).first()
    return electricity

def get_data_electricity(electricity: Electricity) -> dict:
    out = {}
    out = get_prev_data_electricity(out)
    if electricity:
        out['title'] = electricity.title
        out['id'] = electricity.id
        out['payment_date'] = electricity.payment_date
        out['payment_month'] = electricity.payment_month
        out['volume'] = electricity.volume
        out['amount'] = str(electricity.amount)
        out['rate'] = str(electricity.rate)
        out['indications'] = electricity.indications
    else:
        electricity = get_last_electricity()
        if electricity:
            out['title'] = electricity.title
            out['payment_date'] = TODAY()
            out['payment_month'] = get_prev_month()
            out['indications'] = electricity.indications
            out['prev_indications'] = electricity.indications
    return out


def get_prev_data_electricity(out: dict):
    prev_electricity = get_prev_electricity()
    if prev_electricity:
        out['prev_indications'] = prev_electricity.indications
        out['rate'] = str(prev_electricity.rate)
    return out


def set_data_electricity(electricity: Electricity, data: dict) -> bool:
    if not electricity:
        electricity = Electricity()
    try:
        operation = data['operation']
        payment_date = data['payment_date']
        payment_month = data['payment_month']

        indications = data['electricity_indications']
        rate = data['electricity_rate']
        volume = data['electricity_volume']
        amount = data['electricity_amount']

        if not all((rate, indications, volume,)):
            return False

        amount = calculate_electricity_amount(rate, volume)

        electricity.payment_date = payment_date
        electricity.payment_month = payment_month
        electricity.volume = volume
        electricity.rate = rate
        electricity.amount = amount
        electricity.indications = indications
        electricity.save()
        return True
    except TypeError as e:
        log.error('set_data_electricity(): TypeError' + e)
        return False


def calculate_electricity_amount(rate, volume) -> float:
    return float(rate) * int(volume)


def get_info_electricity() -> list:
    electricity = Electricity.objects.filter().order_by('-payment_date').values()
    return electricity


def delete_electricity(electricity_id):
    if electricity_id:
        try:
            Electricity.objects.get(pk=electricity_id).delete()
            return True
        except Electricity.DoesNotExist:
            return False
