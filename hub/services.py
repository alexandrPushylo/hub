from typing import Type

from django.template.defaultfilters import title

from hub.models import Rent, ColdWater, HotWater, Electricity
from hub.models import Debt, Debtor, ExchangeRate
import hub.utilites as U


from logger import getLogger
log = getLogger(__name__)


def get_bills(bill: type[Electricity] | type[HotWater] | type[ColdWater] | type[Rent]) -> dict:
    out = {}
    last_bill = bill.objects.filter().order_by('payment_date').last()
    if last_bill:
        prev_bill = bill.objects.filter(payment_date__lt=last_bill.payment_date).last()
        if prev_bill:
            diff_amount = last_bill.amount - prev_bill.amount
            out['diff_amount'] = diff_amount
            if bill in (Electricity, HotWater, ColdWater):
                diff_indications = last_bill.indications - prev_bill.indications
                out['diff_indications'] = diff_indications

        if bill in (Electricity, HotWater, ColdWater):
            out['indications'] = last_bill.indications
            out['rate'] = last_bill.rate

        out['id'] = last_bill.id
        out['title'] = last_bill.title
        out['description'] = last_bill.description
        out['amount'] = last_bill.amount
        out['payment_date'] = last_bill.payment_date
    return out


def get_info_bills(bill: type[Electricity] | type[HotWater] | type[ColdWater] | type[Rent]) -> dict:
    if bill in (Electricity, HotWater, ColdWater):
        bill = bill.objects.filter().order_by('-payment_date')
    elif bill in (Rent,):
        bill = bill.objects.filter().order_by('-payment_date')

    out = {'title': None, 'bill': []}
    for b in bill:
        out['title'] = b.title
        out['bill'].append(b)
    return out


def set_bills(bill: type[Electricity] | type[HotWater] | type[ColdWater] | type[Rent], data: dict) -> bool:
    try:
        payment_date = data.get('payment_date')
        payment_date = U.datetime.strptime(payment_date, '%Y-%m-%d').date()
        description = data.get('description')
        indications = int(data.get('indications')) if data.get('indications') else None
        rate = float(data.get('rate')) if data.get('rate') else None
        amount = float(data.get('amount')) if data.get('amount') else None

        diff_days = (U.TODAY() - payment_date).days
        last_bill = bill.objects.filter().order_by('payment_date').last()

        if not last_bill or U.TODAY().month > last_bill.payment_date.month or diff_days > 10:
            log.debug('set_bills() - ADD')
            new_bill = bill()
            payment_date = U.TODAY()
        else:
            log.debug('set_bills() - EDIT')
            new_bill = last_bill
        if new_bill:
            new_bill.payment_date = payment_date
            new_bill.description = description
            if bill not in (Rent,):
                new_bill.indications = indications
                new_bill.rate = rate
                new_bill.amount = calculate_amount(rate, indications)
            else:
                new_bill.amount = amount
            new_bill.save()
        else:
            return False
        return True
    except (bill.DoesNotExist, bill.MultipleObjectsReturned):
        return False


def get_inform_data()-> dict:
    out = {
        'today': U.TODAY()
    }
    return out


def calculate_amount(rate: float, indications:int)->float:
    if not indications or not rate:
        raise ValueError('indications and rate are required')
    return float(rate) * int(indications)