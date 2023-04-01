"""em6 sensors"""
from datetime import datetime, timedelta

import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_LOCATION
from homeassistant.helpers.entity import Entity

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

class em6EnergyPriceSensor(Entity):
    def __init__(self, name, api):
        self._name = name
        self._icon = "mdi:chart-bar"
        self._state = None
        self._state_attributes = {}
        self._state_class = "measurement"
        self._unit_of_measurement = '$'
        self._unique_id = DOMAIN
        self._api = api

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def state_class(self):
        """Return the state class of the device."""
        return self._state_class

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._state_attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id

    def update(self):
        _LOGGER.debug('Fetching prices')
        response = self._api.get_prices()
        
        if response:
            _LOGGER.debug('Found price')
            _LOGGER.debug(response)
            
            # Avoid updating the price (state) if the price is still the same or we will get duplicate notifications
            if self._state != response['price'] / 1000:
                self._state = response['price'] / 1000
                self._state_attributes['Trading Period'] = response['trading_period']
                self._state_attributes['Grid Zone'] = response['grid_zone_name']
                self._state_attributes['Last Updated'] = response['timestamp']
        else:
            self._state = None
            _LOGGER.warning('Found no prices on refresh')
