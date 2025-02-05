"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from hub import views as V
from hub import api as API

urlpatterns = [
    path('', V.index, name='index'),
    path('dashboard', V.dashboard_view, name='dashboard'),
    path('edit_bills/', V.edit_bills_view, name='edit_bills'),
    path('delete_bills/', V.delete_bills_view, name='delete_bills'),
    path('info_bills', V.info_bills_view, name='info_bills'),

    path('api/', API.test_api, name='test_api'),
    path('dev', V.dev_view, name='dev'),






    path('admin/', admin.site.urls),
]
