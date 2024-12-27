from django.db import models
# from hub.assets import CURRENCY_CHOICES

# Create your models here.

#   DEBTS   ---------------------------------------------------------------------------
# class Debtor(models.Model):
#     first_name = models.CharField(max_length=120, verbose_name='Имя')
#     last_name = models.CharField(max_length=120, verbose_name='Фамилия')
#     solvency = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Платежеспособность', default=0)

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'

#     class Meta:
#         verbose_name = 'Должник'
#         verbose_name_plural = 'Должники'
#         ordering = ['last_name']


# class Debt(models.Model):
#     title = models.CharField(max_length=256, verbose_name='Название', null=True, blank=True)
#     description = models.TextField(verbose_name='Описание', blank=True, null=True)
#     amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма', blank=True, null=True)
#     currency = models.CharField(max_length=200, verbose_name='Валюта', choices=CURRENCY_CHOICES)
#     date_start_time = models.TimeField(verbose_name='Время создания', blank=True, null=True)
#     date_start_date = models.DateField(verbose_name='Дата создания', blank=True, null=True)
#     date_end = models.DateField(verbose_name='Конечная дата', blank=True, null=True)
#     debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, verbose_name='Должник')
#     is_closed = models.BooleanField(default=False, verbose_name='Закрыто')
#     is_hidden = models.BooleanField(default=False, verbose_name='Скрыто')

#     def __str__(self):
#         return f"{self.debtor} - {self.amount} {self.currency} - {'Закрыто' if self.is_closed else 'Открыто'}"

#     class Meta:
#         verbose_name = 'Долг'
#         verbose_name_plural = 'Долги'
#         ordering = ['date_end']


# class ExchangeRate(models.Model):
#     rate = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Курс')
#     date = models.DateField(verbose_name='Дата')
#     currency = models.CharField(max_length=200, verbose_name='Валюта', choices=CURRENCY_CHOICES)

#     def __str__(self):
#         return f'{self.date} - {self.rate} {self.currency}'

#     class Meta:
#         verbose_name = 'Курс'
#         verbose_name_plural = 'Курсы'
#         ordering = ['date']

#   DEBTS   ---------------------------------------------------------------------------
#   BILLS   ---------------------------------------------------------------------------

class Rent(models.Model):
    title = 'Жировка'
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма')
    payment_date = models.DateField(verbose_name='Дата платежа')

    def __str__(self):
        return f"{self.payment_date} - {self.amount} руб."

    class Meta:
        verbose_name = 'Жировка'
        verbose_name_plural = 'Жировки'
        ordering = ('-payment_date',)


class Gas(models.Model):
    title = 'Газ'
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    indications = models.DecimalField(max_digits=9, decimal_places=3, verbose_name='Показания', max_length=120)
    payment_date = models.DateField(verbose_name='Дата платежа')

    def __str__(self):
        return f"{self.payment_date} - {self.indications}"

    class Meta:
        verbose_name = 'Газ'
        verbose_name_plural = 'Газ'
        ordering = ('-payment_date',)


class ColdWater(models.Model):
    title = 'Холодная вода'
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    indications = models.IntegerField(verbose_name='Показания')
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма', blank=True, null=True)
    rate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name='Тариф')
    payment_date = models.DateField(verbose_name='Дата платежа')

    def __str__(self):
        return f"{self.payment_date} - {self.indications} кубов - {self.amount} руб."

    class Meta:
        verbose_name = 'Холодная вода'
        verbose_name_plural = 'Холодная вода'
        ordering = ('-payment_date',)


class HotWater(models.Model):
    title = 'Горячая вода'
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    indications = models.IntegerField(verbose_name='Показания')
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма', blank=True, null=True)
    rate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name='Тариф')
    payment_date = models.DateField(verbose_name='Дата платежа')

    def __str__(self):
        return f"{self.payment_date} - {self.indications} кубов - {self.amount} руб."

    class Meta:
        verbose_name = 'Горячая вода'
        verbose_name_plural = 'Горячая вода'
        ordering = ('-payment_date',)


class Electricity(models.Model):
    title = 'Электроэнергия'
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    indications = models.IntegerField(verbose_name='Показания')
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма', blank=True, null=True)
    rate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name='Тариф')
    payment_date = models.DateField(verbose_name='Дата платежа')

    def __str__(self):
        return f"{self.payment_date} - {self.indications} кВт/ч - {self.amount} руб."

    class Meta:
        verbose_name = 'Электроэнергия'
        verbose_name_plural = 'Электроэнергия'
        ordering = ('-payment_date',)

#   BILLS   ---------------------------------------------------------------------------


