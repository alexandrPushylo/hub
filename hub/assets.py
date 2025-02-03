from enum import Enum
from typing import NamedTuple, Type

class CurrencyURL(Enum):
    USD = "https://api.nbrb.by/exrates/rates/431"
    EUR = "https://api.nbrb.by/exrates/rates/451"
    RUB = "https://api.nbrb.by/exrates/rates/456"

CURRENCY_CHOICES = (
    ('BYN', 'BYN'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('RUB', 'RUB'),
)

class MONTH(Enum):
    JANUARY = 'January'
    FEBRUARY = 'February'
    MARCH = 'March'
    APRIL = 'April'
    MAY = 'May'
    JUNE = 'June'
    JULY = 'July'
    AUGUST = 'August'
    SEPTEMBER = 'September'
    OCTOBER = 'October'
    NOVEMBER = 'November'
    DECEMBER = 'December'

MONTH_CHOICES = (
    (MONTH.JANUARY.value, 'Январь'),
    (MONTH.FEBRUARY.value, 'Февраль'),
    (MONTH.MARCH.value, 'Март'),
    (MONTH.APRIL.value, 'Апрель'),
    (MONTH.MAY.value, 'Май'),
    (MONTH.JUNE.value, 'Июнь'),
    (MONTH.JULY.value, 'Июль'),
    (MONTH.AUGUST.value, 'Август'),
    (MONTH.SEPTEMBER.value, 'Сентябрь'),
    (MONTH.OCTOBER.value, 'Октябрь'),
    (MONTH.NOVEMBER.value, 'Ноябрь'),
    (MONTH.DECEMBER.value, 'Декабрь'),
)

class Currency(Enum):
    BYN = CURRENCY_CHOICES[0][0]
    USD = CURRENCY_CHOICES[1][0]
    EUR = CURRENCY_CHOICES[2][0]
    RUB = CURRENCY_CHOICES[3][0]


class Bills(Enum):
    ELECTRICITY = 'electricity'
    WATER_SUPPLY = 'water_supply'
    RENT = 'rent'

class Status(Enum):
    OK = 'ok'
    ERROR = 'error'

EDIT_BILLS_TEMPLATES = {
    Bills.WATER_SUPPLY.value: 'bills/edit_water_supply.html',
    Bills.RENT.value: 'bills/edit_rent.html',
    Bills.ELECTRICITY.value: 'bills/edit_electricity.html',
}

INFO_BILLS_TEMPLATES = {
    Bills.WATER_SUPPLY.value: 'bills/info_water_supply.html',
    Bills.RENT.value: 'bills/info_rent.html',
    Bills.ELECTRICITY.value: 'bills/info_electricity.html',
}

TITLE_BILLS = {
    Bills.WATER_SUPPLY.value: 'Водоснабжение',
    Bills.RENT.value: 'Жировка',
    Bills.ELECTRICITY.value: 'Электроэнергия',
}

class NotificationPeriod(Enum):
    NOT = None
    D1 = '1d'
    D3 = '3d'
    D5 = '5d'
    W1 = '1w'
    W2 = '2w'
    W3 = '3w'
    M1 = '1m'
    M2 = '2m'
    M3 = '3m'

NOTIFICATION_PERIOD_CHOICES = (
    (NotificationPeriod.NOT.value, 'Нет'),
    (NotificationPeriod.D1.value, 'За 1 день'),
    (NotificationPeriod.D3.value, 'За 3 дня'),
    (NotificationPeriod.D5.value, 'За 5 дней'),
    (NotificationPeriod.W1.value, 'За 1 неделю'),
    (NotificationPeriod.W2.value, 'За 2 недели'),
    (NotificationPeriod.W3.value, 'За 3 недели'),
    (NotificationPeriod.M1.value, 'За 1 месяц'),
    (NotificationPeriod.M2.value, 'За 2 месяца'),
    (NotificationPeriod.M3.value, 'За 3 месяца'),
)

class PaidPeriod(Enum):
    NOT = None
    D1 = '1d'
    D2 = '2d'
    W1 = '1w'
    W2 = '2w'
    W3 = '3w'
    M1 = '1m'
    M2 = '2m'
    M3 = '3m'
    M6 = '6m'
    Y1 = '1y'

PAID_PERIOD_CHOICES = (
    (PaidPeriod.NOT.value, 'Нет'),
    (PaidPeriod.D1.value, '1 день'),
    (PaidPeriod.D2.value, '2 дня'),
    (PaidPeriod.W1.value, '1 неделя'),
    (PaidPeriod.W2.value, '2 недели'),
    (PaidPeriod.W3.value, '3 недели'),
    (PaidPeriod.M1.value, '1 месяц'),
    (PaidPeriod.M2.value, '2 месяца'),
    (PaidPeriod.M3.value, '3 месяца'),
    (PaidPeriod.M6.value, '6 месяцев'),
    (PaidPeriod.Y1.value, '1 год'),
)
