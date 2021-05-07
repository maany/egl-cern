import hashlib
import certifi
import ssl
import pycountry
from geopy.geocoders import OpenMapQuest
from django.conf import settings
import geopy
import unidecode
from py_expression_eval import Parser
import re
import time
import datetime


def md5_string(str):
    m = hashlib.md5(str.encode('utf-8'))
    return m.hexdigest()


def get_py_country(country):
    py_country = pycountry.countries.get(official_name=country.strip())
    if py_country is None:
        py_country = pycountry.countries.get(name=country.strip())
    return py_country


def get_country(latitude, longitude):
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocation_api_key = settings.GEOLOCATION_API_KEY
    geolocator = OpenMapQuest(api_key=geolocation_api_key)
    output = geolocator.reverse("{latitude}, {longitude}".format(latitude=latitude, longitude=longitude))
    country = output.address.split(',')[-1]
    country = unidecode.unidecode(country)
    py_country = pycountry.countries.get(official_name=country.strip())
    if py_country is None:
        py_country = pycountry.countries.get(name=country.strip())
    return py_country


def get_geo_coords(address):
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocation_api_key = settings.GEOLOCATION_API_KEY
    geolocator = OpenMapQuest(api_key=geolocation_api_key)
    output = geolocator.geocode(address)
    return {
        "latitude": output.latitude,
        "longitude": output.longitude
    }


def parse_influx_eq(equation):
    matches = re.findall('(\d*.)([h,d])', equation)
    for match in matches:
        equation = re.sub(''.join(match), '*'.join(match), equation)
    equation = equation.replace('()','')
    parser = Parser()
    parsed_eq = parser.parse(equation)
    result = parsed_eq.evaluate({
        'now': time.time(),
        'h': 60*60,
        'd': 24*60*60
    })
    return result


def timestamp_datetime(timestamp):
   return datetime.datetime.fromtimestamp(int(timestamp))


def datetime_timestamp(date_time):
    if type(date_time) == type(""):
        date_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M')
    return int(1000000000 * datetime.datetime.timestamp(date_time))


class Singleton:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
