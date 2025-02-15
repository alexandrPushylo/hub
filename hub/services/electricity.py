from datetime import date

from hub.models import Electricity
from logger import getLogger
log = getLogger(__name__)


def get_data(bill_instance: Electricity) -> dict[str, str]:
    return {
        'title': bill_instance.title,
        'id': bill_instance.id,
        'payment_date': bill_instance.payment_date,
        'payment_month': bill_instance.payment_month,

        'volume': bill_instance.volume,
        'amount': str(bill_instance.amount),
        'rate': str(bill_instance.rate),
        'indications': bill_instance.indications,
    }

def get_last_data(bill_instance: Electricity) -> dict[str, str]:
    return {
        'title': bill_instance.title,
        'id': bill_instance.id,
        'payment_date': bill_instance.payment_date,
        'payment_month': bill_instance.payment_month,
        'indications': bill_instance.indications,
        'prev_indications': bill_instance.indications,
    }

def get_prev_data(bill_instance: Electricity) -> dict[str, str]:
    return {
        'prev_indications': bill_instance.indications,
        'rate': str(bill_instance.rate),
    }

def set_data(bill_instance: Electricity, data: dict) -> bool:
    try:
        # operation = data['operation']
        payment_date = data['payment_date']
        payment_month = data['payment_month']

        indications = data['electricity_indications']
        rate = data['electricity_rate']
        volume = data['electricity_volume']
        # amount = data['electricity_amount']

        if not all((
            rate,
            indications,
            volume,
        )):
            log.error('Electricity.set_data() - [not rate, indications, volume]')
            return False

        amount = calculate_electricity_amount(rate, volume)

        bill_instance.payment_date = payment_date
        bill_instance.payment_month = payment_month
        bill_instance.volume = volume
        bill_instance.rate = rate
        bill_instance.amount = amount
        bill_instance.indications = indications
        bill_instance.save()
        return True

    except KeyError:
        log.error('Electricity.set_data() - [KeyError]')
        return False

def calculate_electricity_amount(rate: float, volume: int) -> float:
    return float(rate) * int(volume)

def get_electricity_invoice(payment_month: str, payment_date: date) -> int | None:
    electricity = Electricity.objects.filter(
        payment_month=payment_month,
        payment_date__gte=payment_date,
    ).last()
    if electricity:
        return electricity.volume
    return None