from .types import Enum


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

class Currency(Enum):
    BYN = CURRENCY_CHOICES[0][0]
    USD = CURRENCY_CHOICES[1][0]
    EUR = CURRENCY_CHOICES[2][0]
    RUB = CURRENCY_CHOICES[3][0]


class Bills(Enum):
    ELECTRICITY = 'electricity'
    COLD_WATER = 'cold_water'
    HOT_WATER = 'hot_water'
    RENT = 'rent'

class Status(Enum):
    OK = 'ok'
    ERROR = 'error'
