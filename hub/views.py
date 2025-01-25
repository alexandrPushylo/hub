from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from hub.services import water_supply as WS_
from hub.services import electricity as E_
from hub.services import rent as R_

import hub.services_b as S
import hub.utilites as U
import  hub.assets as A

# Create your views here.

from logger import getLogger
log = getLogger(__name__)


def index(request):
    return render(request, 'base.html', {})


def dashboard_view(request):
    out = {
        'rent': R_.get_data_rent(R_.get_last_rent()),
        'water_supply': WS_.get_data_water_supply(WS_.get_last_water_supply()),
        'electricity': E_.get_data_electricity(E_.get_last_electricity()),
        'inf': S.get_inform_data(),
        'rate': S.check_currency_data(),
    }
    return render(request, 'dashboard.html', out)


def edit_bills_view(request):
    context = {
        'today': U.TODAY(),
        'month_choices': A.MONTH_CHOICES,
    }
    template_name = 'bills/404.html'

    bills_id = request.GET.get('id')
    type_of_bill = request.GET.get('bill')
    type_of_bill = type_of_bill.strip("'") if type_of_bill else None


    match type_of_bill:
        case A.Bills.WATER_SUPPLY.value:
            bill = WS_.get_water_supply_by_id(bills_id)
            data = WS_.get_data_water_supply(bill)
            template_name = 'bills/edit_water_supply.html'
        case A.Bills.ELECTRICITY.value:
            bill = E_.get_electricity_by_id(bills_id)
            data = E_.get_data_electricity(bill)
            template_name = 'bills/edit_electricity.html'
        case A.Bills.RENT.value:
            bill = R_.get_rent_by_id(bills_id)
            data = R_.get_data_rent(bill)
            template_name = 'bills/edit_rent.html'
        case _:
            data = None
    context['bill'] = data

    if request.method == 'POST':
        match type_of_bill:
            case A.Bills.WATER_SUPPLY.value:
                bill = WS_.get_water_supply_by_id(bills_id)
                status = A.Status.OK.value if WS_.set_data_water_supply(bill, request.POST) else A.Status.ERROR.value

            case A.Bills.ELECTRICITY.value:
                bill = E_.get_electricity_by_id(bills_id)
                status = A.Status.OK.value if E_.set_data_electricity(bill, request.POST) else A.Status.ERROR.value

            case A.Bills.RENT.value:
                bill = R_.get_rent_by_id(bills_id)
                status = A.Status.OK.value if R_.set_data_rent(bill, request.POST) else A.Status.ERROR.value
            case _:
                status = A.Status.ERROR.value
        return HttpResponse(status)
    return render(request, template_name, context)


def info_bills_view(request):
    context = {
        'title': '',
        'month_choices': A.MONTH_CHOICES
    }
    template_name = 'bills/info_bills.html'

    bills_id = request.GET.get('id')
    type_of_bill = request.GET.get('bill')
    type_of_bill = type_of_bill.strip("'") if type_of_bill else None

    match type_of_bill:
        case A.Bills.WATER_SUPPLY.value:
            context['title'] = 'Водоснабжение'
            context['bills'] = WS_.get_info_water_supply()
            template_name = 'bills/info_water_supply.html'
        case A.Bills.ELECTRICITY.value:
            context['title'] = 'Электроэнергия'
            context['bills'] = E_.get_info_electricity()
            template_name = 'bills/info_electricity.html'
        case A.Bills.RENT.value:
            context['title'] = 'Жировка'
            context['bills'] = R_.get_info_rent()
            template_name = 'bills/info_rent.html'
        case _:
            context['bills'] = []

    return render(request, template_name, context)


def delete_bills_view(request):
    bills_id = request.GET.get('id')
    type_of_bill = request.GET.get('bill')
    type_of_bill = type_of_bill.strip("'") if type_of_bill else None

    match type_of_bill:
        case A.Bills.WATER_SUPPLY.value:
            WS_.delete_water_supply(bills_id)
        case A.Bills.ELECTRICITY.value:
            E_.delete_electricity(bills_id)
        case A.Bills.RENT.value:
            R_.delete_rent(bills_id)
        case _:
            pass

    return HttpResponseRedirect(f'/info_bills?bill={type_of_bill}')