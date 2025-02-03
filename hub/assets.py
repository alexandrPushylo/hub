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

NOTIFICATION_PERIOD_CHOICES = (
    (None, 'Нет'),
    ('1d', 'За 1 день'),
    ('3d', 'За 3 дня'),
    ('5d', 'За 5 дней'),
    ('1w', 'За 1 неделю'),
    ('2w', 'За 2 недели'),
    ('3w', 'За 3 недели'),
    ('1m', 'За 1 месяц'),
    ('2m', 'За 2 месяца'),
    ('3m', 'За 3 месяца'),
)
PAID_PERIOD_CHOICES = (
    (None, 'Нет'),
    ('1d', '1 день'),
    ('2d', '2 дня'),
    ('1w', '1 неделя'),
    ('2w', '2 недели'),
    ('3w', '3 недели'),
    ('1m', '1 месяц'),
    ('2m', '2 месяца'),
    ('3m', '3 месяца'),
    ('6m', '6 месяцев'),
    ('1y', '1 год'),
)
