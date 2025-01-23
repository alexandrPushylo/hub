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
