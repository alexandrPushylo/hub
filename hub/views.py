from django.shortcuts import render

# Create your views here.

from logger import getLogger
log = getLogger(__name__)


def index(request):
    return render(request, 'base.html', {})


def dashboard_view(request):
    return render(request, 'dashboard.html', {})