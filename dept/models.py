from django.db import models

from assets.assets import CURRENCY_CHOICES

# Create your models here.


class Debtor(models.Model):
    first_name = models.CharField(max_length=120, verbose_name='Имя')
    last_name = models.CharField(max_length=120, verbose_name='Фамилия')
    solvency = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Платежеспособность', default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Должник'
        verbose_name_plural = 'Должники'
        ordering = ['last_name']


class Debt(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма', blank=True, null=True)
    currency = models.CharField(max_length=200, verbose_name='Валюта', choices=CURRENCY_CHOICES)
    date_start_time = models.TimeField(verbose_name='Время создания', blank=True, null=True)
    date_start_date = models.DateField(verbose_name='Дата создания', blank=True, null=True)
    date_end = models.DateField(verbose_name='Конечная дата', blank=True, null=True)
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, verbose_name='Должник')
    is_closed = models.BooleanField(default=False, verbose_name='Закрыто')
    is_hidden = models.BooleanField(default=False, verbose_name='Скрыто')

    def __str__(self):
        return f"{self.debtor} - {self.amount} {self.currency} - {'Закрыто' if self.is_closed else 'Открыто'}"

    class Meta:
        verbose_name = 'Долг'
        verbose_name_plural = 'Долги'
        ordering = ['date_end']

