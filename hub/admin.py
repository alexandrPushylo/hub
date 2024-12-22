from django.contrib import admin
from hub.models import Debt, Debtor, ExchangeRate
# Register your models here.

admin.site.register(Debt)
admin.site.register(Debtor)
admin.site.register(ExchangeRate)
