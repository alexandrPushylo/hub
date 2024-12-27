from django.http import HttpResponse
from django.shortcuts import render


from hub.models import Rent, ColdWater, HotWater, Electricity
import hub.services as S
import hub.utilites as U
import  hub.assets as A

# Create your views here.

from logger import getLogger
log = getLogger(__name__)


def index(request):
    return render(request, 'base.html', {})


def dashboard_view(request):
    out = {
        'rent': S.get_bills(Rent),
        'cold_water': S.get_bills(ColdWater),
        'hot_water': S.get_bills(HotWater),
        'electricity': S.get_bills(Electricity),
        'inf': S.get_inform_data(),
    }

    return render(request, 'dashboard.html', out)


def edit_bills_view(request):
    type_of_bill = request.GET.get('bill')
    type_of_bill = type_of_bill.strip("'") if type_of_bill else None

    match type_of_bill:
        case A.Bills.HOT_WATER.value:
            bill = S.get_bills(HotWater)
        case A.Bills.COLD_WATER.value:
            bill = S.get_bills(ColdWater)
        case A.Bills.ELECTRICITY.value:
            bill = S.get_bills(Electricity)
        case A.Bills.RENT.value:
            bill = S.get_bills(Rent)
        case _:
            bill = None

    if request.method == 'POST':
        match type_of_bill:
            case A.Bills.HOT_WATER.value:
                status = A.Status.OK.value if S.set_bills(HotWater, request.POST) else A.Status.ERROR.value
            case A.Bills.COLD_WATER.value:
                status = A.Status.OK.value if S.set_bills(ColdWater, request.POST) else A.Status.ERROR.value
            case A.Bills.ELECTRICITY.value:
                status = A.Status.OK.value if S.set_bills(Electricity, request.POST) else A.Status.ERROR.value
            case A.Bills.RENT.value:
                status = A.Status.OK.value if S.set_bills(Rent, request.POST) else A.Status.ERROR.value
            case _:
                status = A.Status.ERROR.value
        return HttpResponse(status)

    return render(request, 'bills/edit_bills.html', {'bill': bill})


def info_bills_view(request):
    type_of_bill = request.GET.get('bill')
    type_of_bill = type_of_bill.strip("'") if type_of_bill else None

    match type_of_bill:
        case A.Bills.HOT_WATER.value:
            bill = S.get_info_bills(HotWater)
        case A.Bills.COLD_WATER.value:
            bill = S.get_info_bills(ColdWater)
        case A.Bills.ELECTRICITY.value:
            bill = S.get_info_bills(Electricity)
        case A.Bills.RENT.value:
            bill = S.get_info_bills(Rent)
        case _:
            bill = None

    return render(request, 'bills/info_bills.html', bill)