from typing import Type

from django.template.defaultfilters import title

from hub.models import Rent, ColdWater, HotWater, Electricity
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
            out['indications'] = last_bill.indications
            out['rate'] = last_bill.rate

        out['id'] = last_bill.id
        out['title'] = last_bill.title
        out['description'] = last_bill.description
        out['amount'] = last_bill.amount
        out['payment_date'] = last_bill.payment_date
    return out
def set_bills(bill: type[Electricity] | type[HotWater] | type[ColdWater] | type[Rent], data: dict) -> bool:
    try:
        last_bill = bill.objects.filter().order_by('payment_date').last()
        if not last_bill:
            return False
        diff_days = (U.TODAY() - last_bill.payment_date).days
        if U.TODAY().month > last_bill.payment_date.month or diff_days > 10:
            print('add')
            new_bill = bill.objects.create()
        else:
            print('edit')
            new_bill = last_bill
        if new_bill:
            new_bill.payment_date = data.get('payment_date')
            new_bill.amount = data.get('amount')
            new_bill.description = data.get('description')
            if bill not in (Rent,):
                new_bill.indications = data.get('indications')
                new_bill.rate = data.get('rate')
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