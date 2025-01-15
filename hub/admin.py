from django.contrib import admin
from hub.models import Debt, Debtor, ExchangeRate
from hub.models import Rent, Gas, ColdWater, HotWater, Electricity
# Register your models here.

admin.site.register(Debt)
admin.site.register(Debtor)




@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('date', 'rate', 'currency', 'scale')


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'amount')


@admin.register(Gas)
class GasAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'indications')


@admin.register(ColdWater)
class ColdWaterAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'indications', 'amount')


@admin.register(HotWater)
class HotWaterAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'indications', 'amount')


@admin.register(Electricity)
class ElectricityAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'indications', 'amount')
