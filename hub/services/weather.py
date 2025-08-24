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
            'temp': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'temp_min': round(data['main']['temp_min']),
            'temp_max': round(data['main']['temp_max']),
            'weather_main': data['weather'][0]['main'],
            'weather_description': str(data['weather'][0]['description']).capitalize(),
            'weather_icon_srs': get_icon_weather(data['weather'][0]['icon']),
        }
    except KeyError as e:
        log.error('get_main_indicators() - [KeyError]' + str(e))
        return {}


def get_icon_weather(icon: str):
    url = f"http://openweathermap.org/img/w/{icon}.png"
    return url