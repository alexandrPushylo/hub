from django.contrib import admin
# from hub.models import Debt, Debtor, ExchangeRate
from hub.models import Rent, Gas, ColdWater, HotWater, Electricity
# Register your models here.

# admin.site.register(Debt)
# admin.site.register(Debtor)
# admin.site.register(ExchangeRate)

admin.site.register(Rent)
admin.site.register(Gas)
admin.site.register(ColdWater)
admin.site.register(HotWater)
admin.site.register(Electricity)
