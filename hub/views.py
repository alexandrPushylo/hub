from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from hub.models import Electricity, Rent, Water
import hub.utilites as U
import  hub.assets as A

# Create your views here.

from logger import getLogger
log = getLogger(__name__)


def index(request):
    return render(request, 'base.html', {})


@U.check_is_authenticated
def dashboard_view(request):
    out = {
        'rent': U.get_data_last_bill(Rent),
        'water_supply': U.get_data_last_bill(Water),
        'electricity': U.get_data_last_bill(Electricity),
        'inf': U.get_inform_data(),
        'rate': U.get_current_currency_data(),
        'subs': U.get_subs_data_for_dashboard(),
        'bills': U.get_bills_data_for_dashboard(),
    }
    return render(request, 'dashboard.html', out)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/dashboard')


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        password = request.POST.get('password')
        user = U.get_current_user()
        if user is None:
            return HttpResponseRedirect('/login')
        user = authenticate(request, username=user.username, password=password)
        login(request, user)
        return HttpResponseRedirect('/dashboard')


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


@U.check_is_authenticated
def info_bills_view(request):
    context = {
        'title': '',
        'month_choices': A.MONTH_CHOICES
    }
    template_name = '404.html'

    bills_id = request.GET.get('id')
    type_of_bill = request.GET.get('bill')

    if type_of_bill:
        template_name = A.INFO_BILLS_TEMPLATES[type_of_bill]
        context['title'] = A.TITLE_BILLS[type_of_bill]
        bill_type = U.get_bill_type(type_of_bill)
        context['bills'] = U.get_list_bill(bill_type)

    return render(request, template_name, context)


@U.check_is_authenticated
def delete_bills(request):
    bills_id = request.GET.get('id')
    type_of_bill = request.GET.get('bill')

    if type_of_bill:
        bill_type = U.get_bill_type(type_of_bill)
        U.delete_bill(bills_id, bill_type)
    return HttpResponseRedirect(f'/info_bills?bill={type_of_bill}')


@U.check_is_authenticated
def subscriptions_view(request):
    context = {}
    template_name = 'subscriptions/subscriptions.html'

    subscriptions = U.get_subscriptions_value()
    context['subscriptions'] = subscriptions
    if not subscriptions:
        return HttpResponseRedirect(f'/dashboard')

    return render(request, template_name, context)


@U.check_is_authenticated
def subscription_view(request):
    context = {}
    template_name = '404.html'
    subscription_id = request.GET.get('id')

    if subscription_id:
        template_name = 'subscriptions/item_subscription.html'
        subs_dict = U.get_subs_to_dict(subscription_id)
        context['subscription'] = subs_dict
        context['subscription']['notification_period'] = U.get_str_notification(subs_dict['notification_period'])
        context['subscription']['paid_period'] = U.get_str_paid_period(subs_dict['paid_period'])
        context['subscription']['next_payment'] = U.SUB_S.get_str_next_payment_date(subs_dict['next_payment_date'])
    return render(request, template_name, context)


@U.check_is_authenticated
def edit_subscription_view(request):
    context = {}
    template_name = 'subscriptions/edit_subscription.html'
    subscription_id = request.GET.get('id')

    context['categories'] = U.SUB_S.get_categories()
    context['paid_period_choices'] = A.PAID_PERIOD_CHOICES
    context['notification_period_choices'] = A.NOTIFICATION_PERIOD_CHOICES
    context['currencies'] = A.CURRENCY_CHOICES

    if subscription_id:
        subs_dict = U.get_subs_to_dict(subscription_id)
        context['subscription'] = subs_dict
        # context['subscription']['notification_period'] = U.get_str_notification(subs_dict['notification_period'])
        # context['subscription']['paid_period'] = U.get_str_paid_period(subs_dict['paid_period'])
        context['subscription']['next_payment'] = U.SUB_S.get_str_next_payment_date(subs_dict['next_payment_date'])
    else:
        # ADD MODE
        pass

    if request.method == "POST":
        U.set_data_subscription(request.POST.get('id'), request.POST, request.FILES)
        return HttpResponseRedirect(f'/subscriptions')
    return render(request, template_name, context)


@U.check_is_authenticated
def deactivate_subscription(request):
    subscriptions_id = request.GET.get('id')

    status = U.SUB_S.deactivate_subscription(subscriptions_id) if subscriptions_id else None

    if status:
        return HttpResponseRedirect(f'/subscriptions')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@U.check_is_authenticated
def get_invoice(request):
    context = U.get_invoice_data()

    return render(request, 'bills/invoice.html', context)


@U.check_is_authenticated
def dev_view(request):
    context = {}
    template_name = 'dev.html'

    return render(request, template_name, context)


