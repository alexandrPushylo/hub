from .types import Enum
CURRENCY_CHOICES = {
    'BYN': 'BYN',
    'USD': 'USD',
    'EUR': 'EUR',
    'RUB': 'RUB',
}

class Currency(Enum):
    BYN = CURRENCY_CHOICES['BYN']
    USD = CURRENCY_CHOICES['USD']
    EUR = CURRENCY_CHOICES['EUR']
    RUB = CURRENCY_CHOICES['RUB']


class Bills(Enum):
    ELECTRICITY = 'electricity'
    COLD_WATER = 'cold_water'
    HOT_WATER = 'hot_water'
    RENT = 'rent'

class Status(Enum):
    OK = 'ok'
    ERROR = 'error'
