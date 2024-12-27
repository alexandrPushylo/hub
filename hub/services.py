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
def get_inform_data()-> dict:
    out = {
        'today': U.TODAY()
    }
    return out