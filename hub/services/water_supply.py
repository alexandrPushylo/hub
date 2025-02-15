from datetime import date

from hub.models import Water
from logger import getLogger
log = getLogger(__name__)


def get_data(bill_instance: Water) -> dict[str, str]:
    return {
        'title': bill_instance.title,
        'id': bill_instance.id,
        'payment_date': bill_instance.payment_date,
        'payment_month': bill_instance.payment_month,
        'cold_water_indications': bill_instance.cold_water_indications,
        'hot_water_indications': bill_instance.hot_water_indications,
        'cold_water_volume': bill_instance.cold_water_volume,
        'hot_water_volume': bill_instance.hot_water_volume,
        'total_water_volume': bill_instance.total_water_volume,
        'total_water_amount': str(bill_instance.total_water_amount),
        'water_rate': bill_instance.water_rate,
        'water_heating_volume': str(bill_instance.water_heating_volume),
        'water_heating_rate': str(bill_instance.water_heating_rate),
        'water_heating_amount': str(bill_instance.water_heating_amount),
    }

def get_last_data(bill_instance: Water) -> dict[str, str]:
    return {
        'title': bill_instance.title,
        'id': bill_instance.id,
        'payment_date': bill_instance.payment_date,
        'payment_month': bill_instance.payment_month,
        'cold_water_indications': bill_instance.cold_water_indications,
        'hot_water_indications': bill_instance.hot_water_indications,
    }

def get_prev_data(bill_instance: Water) -> dict[str, str]:
    return {
        'prev_cold_water_indications': bill_instance.cold_water_indications,
        'prev_hot_water_indications': bill_instance.hot_water_indications,
        'water_rate': str(bill_instance.water_rate),
    }

def set_data(bill_instance: Water, data: dict) -> bool:
    try:
        # operation = data['operation']
        payment_date = data['payment_date']
        payment_month = data['payment_month']

        cold_water_indications = data['cold_water_indications']
        hot_water_indications = data['hot_water_indications']
        water_rate = data['water_rate']
        water_heating_rate = data['water_heating_rate']
        cold_water_volume = data['cold_water_volume']
        hot_water_volume = data['hot_water_volume']
        # total_water_volume = data['total_water_volume']
        # total_water_amount = data['total_water_amount']
        water_heating_volume = data['water_heating_volume']
        # water_heating_amount = data['water_heating_amount']

        if not all((
                hot_water_volume,
                cold_water_volume,
        )):
            log.error('Water.set_data() - [not hot_water_volume, cold_water_volume]')
            return False

        total_water_volume = calculate_total_water_volume(hot_water_volume, cold_water_volume)
        total_water_amount = calculate_water_amount(water_rate, total_water_volume)
        water_heating_amount = calculate_water_heating_amount(water_heating_rate, water_heating_volume)

        bill_instance.payment_date = payment_date
        bill_instance.payment_month = payment_month
        bill_instance.cold_water_indications = cold_water_indications
        bill_instance.hot_water_indications = hot_water_indications
        bill_instance.water_rate = water_rate
        bill_instance.water_heating_rate = water_heating_rate
        bill_instance.cold_water_volume = cold_water_volume
        bill_instance.hot_water_volume = hot_water_volume
        bill_instance.water_heating_volume = water_heating_volume

        bill_instance.total_water_volume = total_water_volume
        bill_instance.total_water_amount = total_water_amount
        bill_instance.water_heating_amount = water_heating_amount
        bill_instance.save()
        return True

    except KeyError:
        log.error('Water.set_data() - [KeyError]')
        return False



def calculate_total_water_volume(hot_water_volume: int, cold_water_volume: int) -> int:
    return int(hot_water_volume) + int(cold_water_volume)


def calculate_water_amount(water_rate: float, total_water_volume: int) -> float:
    return float(water_rate) * int(total_water_volume)


def calculate_water_heating_amount(water_heating_rate: float, water_heating_volume: float) -> float:
    return float(water_heating_rate) * float(water_heating_volume)


def get_water_invoice(payment_month: str, payment_date: date) -> dict:
    water = Water.objects.filter(
        payment_month=payment_month,
        payment_date__gte=payment_date
    ).last()
    if water:
        return {
            'cold_water': water.cold_water_volume,
            'hot_water': water.hot_water_volume,
        }
    return {}