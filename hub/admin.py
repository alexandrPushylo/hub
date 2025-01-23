from django.contrib import admin
from hub.models import Debt, Debtor, ExchangeRate
from hub.models import Rent
from hub.models import Electricity
from hub.models import Water
# Register your models here.

admin.site.register(Debt)
admin.site.register(Debtor)




@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('date', 'rate', 'currency', 'scale')


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'amount')


@admin.register(Water)
class WaterAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'cold_water_indications', 'hot_water_indications', 'total_water_amount')


@admin.register(Electricity)
class ElectricityAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'indications', 'amount')
