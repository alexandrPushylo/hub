from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from hub.models import Electricity, Rent, Water

from hub.services import water_supply as WS_
from hub.services import electricity as E_
from hub.services import rent as R_
from hub.services import exchange_rate as ER_

import hub.utilites as U
import  hub.assets as A

# Create your views here.

from logger import getLogger
log = getLogger(__name__)


def index(request):
    return render(request, 'base.html', {})


def dashboard_view(request):
    out = {
        'rent': U.get_data_last_bill(Rent),
        'water_supply': U.get_data_last_bill(Water),
        'electricity': U.get_data_last_bill(Electricity),
        # 'inf': S.get_inform_data(),
        'rate': ER_.check_currency_data(),
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
    bill_type = U.get_bill_type(type_of_bill)

    if bill_type:
        context['bill'] = U.get_data_for_edit_view(bills_id, bill_type)
        template_name = A.EDIT_BILLS_TEMPLATES[type_of_bill]

    if request.method == "POST":
        if bills_id:
            bills_instance = U.get_bill_by_id(bills_id, bill_type)
        else:
            bills_instance = bill_type()
        status = U.set_data_bill(bills_instance, request.POST)
        return HttpResponse(status)
    return render(request, template_name, context)


def info_bills_view(request):
    context = {
        'title': '',
        'month_choices': A.MONTH_CHOICES
    }
    template_name = 'bills/404.html'

    bills_id = request.GET.get('id')
    type_of_bill = request.GET.get('bill')

    if type_of_bill:
        template_name = A.INFO_BILLS_TEMPLATES[type_of_bill]
        context['title'] = A.TITLE_BILLS[type_of_bill]
        bill_type = U.get_bill_type(type_of_bill)
        context['bills'] = U.get_list_bill(bill_type)

    return render(request, template_name, context)


def delete_bills_view(request):
    bills_id = request.GET.get('id')
    type_of_bill = request.GET.get('bill')

    if type_of_bill:
        bill_type = U.get_bill_type(type_of_bill)
        U.delete_bill(bills_id, bill_type)
    return HttpResponseRedirect(f'/info_bills?bill={type_of_bill}')


def dev_view(request):
    context = {}
    template_name = 'dev.html'
    return render(request, template_name, context)