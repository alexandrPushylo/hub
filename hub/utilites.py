from datetime import date, datetime, timedelta

from hub.models import Rent, Water, Electricity
from hub.models import Debt, Debtor, ExchangeRate
from hub.assets import MONTH_CHOICES

from logger import getLogger

log = getLogger(__name__)

TODAY = date.today
NOW = datetime.now().time
MONTH = datetime.now().month


def get_ru_month(month_eng: str) -> str:
    for month in MONTH_CHOICES:
        if month[0] == month_eng:
            return month[1]

def get_prev_month() -> str:
    return MONTH_CHOICES[MONTH-2][0]

