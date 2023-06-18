"""Remko Sensor Integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""

    # Data that you want to share with your platforms
    hass.data[DOMAIN] = {
        'storage_water_temp': 0,
        'current_water_temp': 0,
        'current_outside_temp': 0,
        'current_heating_circuit_temp': 0,
        'current_heating_water_temp': 0,
        'current_power': 0,
        'current_operating_status': None,
        'current_status_heating': None,
        'current_status_hot_water': None,
    }

    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True
