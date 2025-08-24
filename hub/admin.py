from django.contrib import admin
from hub.models import ExchangeRate
from hub.models import Rent
from hub.models import Electricity
from hub.models import Water
from hub.models import SubscriptionsCategory, Subscriptions
# Register your models here.


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
    list_display = ('payment_date', 'volume', 'amount')


@admin.register(SubscriptionsCategory)
class SubscriptionsCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'next_payment_date', 'amount',)
    list_display_links = ('title',)
