from django.shortcuts import render

from hub.models import Rent, ColdWater, HotWater, Electricity
import hub.services as S
# Create your views here.

from logger import getLogger
log = getLogger(__name__)


def index(request):
    return render(request, 'base.html', {})


def dashboard_view(request):
    return render(request, 'dashboard.html', {})    out = {
        'rent': S.get_bills(Rent),
        'cold_water': S.get_bills(ColdWater),
        'hot_water': S.get_bills(HotWater),
        'electricity': S.get_bills(Electricity),
        'inf': S.get_inform_data(),
    }

    return render(request, 'dashboard.html', out)
