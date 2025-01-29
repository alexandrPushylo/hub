import json
import hub.assets as A
import hub.utilites as U
from config.creds import WEATHER_API_KEY

from logger import getLogger
log = getLogger(__name__)

CITY = 'Minsk'
URL_server = 'https://api.openweathermap.org/data/2.5/weather'
spec_props = '&units=metric&lang=ru&appid='

URL = f'{URL_server}?q={CITY}{spec_props}{WEATHER_API_KEY}'

def get_main_indicators(data: dict) -> dict:
    try:
        return {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
        }
    except KeyError as e:
        log.error('get_main_indicators() - [KeyError]' + str(e))
        return {}

