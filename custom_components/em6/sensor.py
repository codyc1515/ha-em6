"""em6 sensors"""
from datetime import datetime, timedelta

import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import CONF_LOCATION

from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .api import em6Api

from .const import (
    DOMAIN,
    SENSOR_NAME
)

NAME = DOMAIN
ISSUEURL = "https://github.com/codyc1515/hacs_em6/issues"

STARTUP = f"""
-------------------------------------------------------------------
{NAME}
This is a custom component
If you have any issues with this you need to open an issue here:
{ISSUEURL}
-------------------------------------------------------------------
"""

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LOCATION): cv.string
})

SCAN_INTERVAL = timedelta(minutes=30)

async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    location = config.get(CONF_LOCATION)

    api = em6Api(location)

    _LOGGER.debug('Setting up sensor(s)...')

    sensors = []
    sensors .append(em6EnergyPriceSensor(SENSOR_NAME, api))
    async_add_entities(sensors, True)

class em6EnergyPriceSensor(SensorEntity):
    def __init__(self, name, api):
        self._attr_name = name
        self._attr_icon = "mdi:chart-bar"
        self._attr_native_value = None
        self._attr_state_attributes = {}
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = 'NZD/kWh'
        self._attr_unique_id = DOMAIN
        self._api = api

    def update(self):
        _LOGGER.debug('Fetching prices')
        response = self._api.get_prices()
        
        if response:
            _LOGGER.debug('Found price')
            _LOGGER.debug(response)
            
            # Avoid updating the price (state) if the price is still the same or we will get duplicate notifications
            if self._attr_native_value != response['price'] / 1000:
                self._attr_native_value = response['price'] / 1000
                self._attr_state_attributes['Trading Period'] = response['trading_period']
                self._attr_state_attributes['Grid Zone'] = response['grid_zone_name']
                self._attr_state_attributes['Last Updated'] = response['timestamp']
        else:
            self._attr_native_value = None
            _LOGGER.warning('Found no prices on refresh')
