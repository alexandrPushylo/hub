from hub.models import ExchangeRate

import hub.assets as A
import hub.utilites as U

from logger import getLogger
log = getLogger(__name__)


def get_currency_data(currency_url: A.CurrencyURL) -> dict:
    response = U.requests.get(currency_url.value)
    return response.json()


def convert_currency(amount: int, to_currency: A.CurrencyURL, reverse: bool = False) -> float:
    """Конвертировать волюту

    Args:
        amount (int): Сумма в белоруских рублях.
        to_currency (Currency): Конвертировать в валюту Currency.
        reverse (bool, optional): Обратная конвертация. По умолчанию False.
    """
    currency_data = get_currency_data(to_currency)
    cur_scale = int(currency_data.get('Cur_Scale'))
    cur_rate = float(currency_data.get('Cur_OfficialRate'))
    amount = int(amount)

    if reverse:
        out = (amount / cur_scale) * cur_rate
    else:
        out = (amount * cur_scale) / cur_rate
    return out


def check_currency_data():
    today = U.TODAY()
    currency_usd = ExchangeRate.objects.filter(currency=A.Currency.USD.value, date=today)
    currency_eur = ExchangeRate.objects.filter(currency=A.Currency.EUR.value, date=today)
    currency_rub = ExchangeRate.objects.filter(currency=A.Currency.RUB.value, date=today)

    if currency_usd.exists():
        usd = currency_usd.first()
    else:
        usd = prepare_currency_data(A.CurrencyURL.USD)

    if currency_eur.exists():
        eur = currency_eur.first()
    else:
        eur = prepare_currency_data(A.CurrencyURL.EUR)

    if currency_rub.exists():
        rub = currency_rub.first()
    else:
        rub = prepare_currency_data(A.CurrencyURL.RUB)

    return {
        'usd': usd,
        'eur': eur,
        'rub': rub
    }


def prepare_currency_data(currency_url: A.CurrencyURL):
    currency_data = get_currency_data(currency_url)
    if currency_data:
        date = U.TODAY()
        rate = currency_data.get('Cur_OfficialRate')
        currency = currency_url.name
        scale = currency_data.get('Cur_Scale')

        try:
            prev_exc_rate = ExchangeRate.objects.get(
                date=date - U.timedelta(days=1),
                currency=currency,
            )
            difference = round(float(rate) - float(prev_exc_rate.rate), 2)
        except ExchangeRate.DoesNotExist:
            difference = 0

        exc_rate = ExchangeRate.objects.create(
            rate=rate,
            date=date,
            currency=currency,
            scale=scale,
            difference=difference,
        )
        return exc_rate