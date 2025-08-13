"""em6 API"""
import logging
from datetime import datetime, timedelta
import requests
import json

_LOGGER = logging.getLogger(__name__)

class em6Api:
    def __init__(self, location):
        self._location = location
        self._url_base = 'https://api.em6.co.nz/ords/em6/data_api/'

    def get_prices(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54"
        }
        try:
            response = requests.get(self._url_base + "region/price", headers=headers)
        except requests.exceptions.RequestException as err:
            _LOGGER.error('Failed to fetch prices: %s', err)
            return None

        if response.status_code == requests.codes.ok:
            data = response.json()
            if not data:
                _LOGGER.warning('Fetched prices successfully, but did not find any')

            if data.get('items'):
                for location in data['items']:
                    if location['grid_zone_name'] == self._location:
                        return location
        else:
            _LOGGER.error('Failed to fetch prices: %s', response.status_code)
            return None
