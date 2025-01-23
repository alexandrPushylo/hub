from django.db.models import QuerySet

from hub.models import Water
from hub.utilites import TODAY, get_prev_month, MONTH

from logger import getLogger

log = getLogger(__name__)


def get_water_supply_by_id(bills_id):
    if bills_id is None:
        water_supply = Water.objects.filter(payment_month=get_prev_month(), payment_date__month=MONTH)
        if water_supply.exists():
            return water_supply.last()
    try:
        return Water.objects.get(id=bills_id)
    except Water.DoesNotExist:
        return None


# def get_water_supply(water_supply_id) -> Water | None:
#     if not water_supply_id:
#         return None
#     try:
#         water_supply = Water.objects.get(id=water_supply_id)
#         return water_supply
#     except Water.DoesNotExist:
#         return None

def get_last_water_supply() -> Water:
    water_supply = Water.objects.filter().order_by('payment_date').last()
    return water_supply

def get_prev_water_supply() -> Water:
    last_water_supply = get_last_water_supply()
    water_supply = Water.objects.filter(payment_date__lt=last_water_supply.payment_date).first()
    return water_supply

def get_data_water_supply(water_supply: Water) -> dict:
    out = {}
    if water_supply:
        out['title'] = water_supply.title
        out['id'] = water_supply.id
        out['payment_date'] = water_supply.payment_date
        out['payment_month'] = water_supply.payment_month
        out['cold_water_indications'] = water_supply.cold_water_indications
        out['hot_water_indications'] = water_supply.hot_water_indications
        out['cold_water_volume'] = water_supply.cold_water_volume
        out['hot_water_volume'] = water_supply.hot_water_volume
        out['total_water_volume'] = water_supply.total_water_volume
        out['total_water_amount'] = str(water_supply.total_water_amount)
        out['water_rate'] = water_supply.water_rate
        out['water_heating_volume'] = str(water_supply.water_heating_volume)
        out['water_heating_rate'] = str(water_supply.water_heating_rate)
        out['water_heating_amount'] = str(water_supply.water_heating_amount)
    else:
        water_supply = get_last_water_supply()
        if water_supply:
            out['title'] = water_supply.title
            out['payment_date'] = TODAY()
            out['payment_month'] = get_prev_month()
            out['cold_water_indications'] = water_supply.cold_water_indications
            out['hot_water_indications'] = water_supply.hot_water_indications

            out['water_heating_volume'] = str(water_supply.water_heating_volume)
            out['water_heating_rate'] = str(water_supply.water_heating_rate)
    out = get_prev_data_water_supply(out)
    return out

def get_prev_data_water_supply(out: dict):
    prev_water_supply = get_prev_water_supply()
    if prev_water_supply:
        out['prev_cold_water_indications'] = prev_water_supply.cold_water_indications
        out['prev_hot_water_indications'] = prev_water_supply.hot_water_indications
        out['water_rate'] = str(prev_water_supply.water_rate)
    return out

def set_data_water_supply(water_instance: Water, data: dict) -> bool:
    if not water_instance:
        water_instance = Water()
    try:
        operation = data['operation']
        payment_date = data['payment_date']
        payment_month = data['payment_month']

        cold_water_indications = data['cold_water_indications']
        hot_water_indications = data['hot_water_indications']
        water_rate = data['water_rate']
        water_heating_rate = data['water_heating_rate']
        cold_water_volume = data['cold_water_volume']
        hot_water_volume = data['hot_water_volume']
        total_water_volume = data['total_water_volume']
        total_water_amount = data['total_water_amount']
        water_heating_volume = data['water_heating_volume']
        water_heating_amount = data['water_heating_amount']

        if not all((
                hot_water_volume,
                cold_water_volume,
        )):
            return False

        total_water_volume = calculate_total_water_volume(hot_water_volume, cold_water_volume)
        total_water_amount = calculate_water_amount(water_rate, total_water_volume)
        water_heating_amount = calculate_water_heating_amount(water_heating_rate, water_heating_volume)

        water_instance.payment_date = payment_date
        water_instance.payment_month = payment_month
        water_instance.cold_water_indications = cold_water_indications
        water_instance.hot_water_indications = hot_water_indications
        water_instance.water_rate = water_rate
        water_instance.water_heating_rate = water_heating_rate
        water_instance.cold_water_volume = cold_water_volume
        water_instance.hot_water_volume = hot_water_volume
        water_instance.water_heating_volume = water_heating_volume

        water_instance.total_water_volume = total_water_volume
        water_instance.total_water_amount = total_water_amount
        water_instance.water_heating_amount = water_heating_amount
        water_instance.save()
        return True
    except TypeError as e:
        log.error('set_data_water_supply(): TypeError' + e)
        return False



def calculate_total_water_volume(hot_water_volume, cold_water_volume) -> int:
    return int(hot_water_volume) + int(cold_water_volume)


def calculate_water_amount(water_rate, total_water_volume) -> float:
    return float(water_rate) * int(total_water_volume)


def calculate_water_heating_amount(water_heating_rate, water_heating_volume) -> float:
    return float(water_heating_rate) * float(water_heating_volume)


def get_info_water_supply() -> list:
    water_supply = Water.objects.filter().order_by('-payment_date').values()
    return water_supply


def delete_water_supply(water_supply_id):
    if water_supply_id:
        try:
            Water.objects.get(pk=water_supply_id).delete()
            return True
        except Water.DoesNotExist:
            return False
