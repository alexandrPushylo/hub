from django.db import models
from hub.assets import CURRENCY_CHOICES, MONTH_CHOICES, NOTIFICATION_PERIOD_CHOICES, PAID_PERIOD_CHOICES

# Create your models here.

#   DEBTS   ---------------------------------------------------------------------------
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


class ExchangeRate(models.Model):
    rate = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Курс')
    date = models.DateField(verbose_name='Дата')
    currency = models.CharField(max_length=200, verbose_name='Валюта', choices=CURRENCY_CHOICES)
    scale = models.IntegerField(default=1, verbose_name='Масштаб')
    difference = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='Разница')

    def __str__(self):
        return f'{self.date} :: {self.scale} BYN = {self.rate} {self.currency}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['date']

#   DEBTS   ---------------------------------------------------------------------------
#   BILLS   ---------------------------------------------------------------------------

class Rent(models.Model):
    title = 'Жировка'
    payment_date = models.DateField(verbose_name='Дата платежа')
    payment_month = models.CharField(max_length=9, verbose_name='Оплачиваемый месяц', choices=MONTH_CHOICES)
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма')


    def __str__(self):
        return f"{self.payment_date} - {self.amount} руб."

    class Meta:
        verbose_name = 'Жировка'
        verbose_name_plural = 'Жировки'
        ordering = ('-payment_date',)


class Water(models.Model):
    title = 'Водоснабжение'
    payment_date = models.DateField(verbose_name='Дата платежа')
    payment_month = models.CharField(max_length=9, verbose_name='Оплачиваемый месяц', choices=MONTH_CHOICES)

    cold_water_indications = models.IntegerField(verbose_name='Показания холодной воды')
    hot_water_indications = models.IntegerField(verbose_name='Показания горячей воды')
    cold_water_volume = models.IntegerField(verbose_name='Объем израсходованной холодной воды', default=0)
    hot_water_volume = models.IntegerField(verbose_name='Объем израсходованной горячей воды', default=0)
    total_water_volume = models.IntegerField(verbose_name='Общий объем израсходованной воды', default=0)
    total_water_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                             verbose_name='Общая сумма за водоснабжение', blank=True, null=True)
    water_rate = models.DecimalField(max_digits=7, decimal_places=4, verbose_name='Тариф на водоснабжение')

    water_heating_volume = models.DecimalField(max_digits=7, decimal_places=4, verbose_name='Подогрев воды Гкал.')
    water_heating_rate = models.DecimalField(max_digits=9, decimal_places=4, verbose_name='Подогрев воды тариф.')
    water_heating_amount = models.DecimalField(max_digits=9, decimal_places=2,
                                             verbose_name='Общая сумма за подогрев воды', blank=True, null=True)


    def __str__(self):
        return f"{self.payment_date} - {self.total_water_volume} кубов - {self.total_water_amount} руб."

    class Meta:
        verbose_name = 'Водоснабжение'
        verbose_name_plural = 'Водоснабжение'
        ordering = ('-payment_date',)


class Electricity(models.Model):
    title = 'Электроэнергия'
    indications = models.IntegerField(verbose_name='Показания, кВт/ч.')
    volume = models.IntegerField(verbose_name='Израсходовано, кВт/ч.', default=0)

    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма', blank=True, null=True)
    rate = models.DecimalField(max_digits=7, decimal_places=4, verbose_name='Тариф')
    payment_date = models.DateField(verbose_name='Дата платежа')
    payment_month = models.CharField(max_length=9, verbose_name='Оплачиваемый месяц', choices=MONTH_CHOICES)

    def __str__(self):
        return f"{self.payment_date} - {self.volume} кВт/ч - {self.amount} руб."

    class Meta:
        verbose_name = 'Электроэнергия'
        verbose_name_plural = 'Электроэнергия'
        ordering = ('-payment_date',)

#   BILLS   ---------------------------------------------------------------------------
#   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
#   SUBSCRIPTIONS   ---------------------------------------------------------------------------

def get_logo_directory_path(instance, filename):
    return "logos/{0}/{1}".format(str(instance.id), filename)

class SubscriptionsCategory(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)


class Subscriptions(models.Model):
    logo = models.ImageField(upload_to=get_logo_directory_path, verbose_name='Лого')
    title = models.CharField(max_length=256, verbose_name='Название подписки')
    category = models.ForeignKey(SubscriptionsCategory, verbose_name='Название категории', on_delete=models.SET_NULL, null=True, blank=True)

    start_of_subscription = models.DateField(verbose_name='Дата начала подписки')
    next_payment_date = models.DateField(verbose_name='Дата следующей оплаты', null=True, blank=True)
    paid_period = models.CharField(max_length=32, verbose_name='Оплачиваемый промежуток', choices=PAID_PERIOD_CHOICES, default=None)
    notification_period = models.CharField(max_length=32, verbose_name='Период уведомления', choices=NOTIFICATION_PERIOD_CHOICES, default=None)
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Сумма', blank=True, null=True)
    currency = models.CharField(max_length=3, verbose_name='Валюта', choices=CURRENCY_CHOICES, default='BYN')
    total_paid_for = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Всего уплачено', blank=True, null=True)

    link = models.CharField(max_length=512, verbose_name='Ссылка', null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    date_of_creation = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.title} :: {self.next_payment_date}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('title',)

#   SUBSCRIPTIONS   ---------------------------------------------------------------------------


