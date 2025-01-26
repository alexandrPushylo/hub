from hub.models import Rent
from logger import getLogger
log = getLogger(__name__)


def get_data(bill_instance: Rent) -> dict[str, str]:
    return {
        'title': bill_instance.title,
        'id': bill_instance.id,
        'payment_date': bill_instance.payment_date,
        'payment_month': bill_instance.payment_month,
        'amount': str(bill_instance.amount),
    }

def get_last_data(bill_instance: Rent) -> dict[str, str]:
    return {
        'title': bill_instance.title,
        'payment_date': bill_instance.payment_date,
        'payment_month': bill_instance.payment_month,
    }

def get_prev_data(bill_instance: Rent) -> dict[str, str]:
    return {}

def set_data(bill_instance: Rent, data: dict) -> bool:
    try:
        # operation = data['operation']
        payment_date = data['payment_date']
        payment_month = data['payment_month']
        amount = data['rent_amount']

        bill_instance.payment_date = payment_date
        bill_instance.payment_month = payment_month
        bill_instance.amount = amount
        bill_instance.save()
        return True

    except KeyError:
        log.error('Rent.set_data() - [KeyError]')
        return False
