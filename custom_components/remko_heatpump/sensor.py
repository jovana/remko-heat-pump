"""Remko Sensor integration (YAML platform, no discovery)."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN
from .remko import RemkoHeatpump

_LOGGER = logging.getLogger(__name__)

# Polling interval (adjust if you want slower/faster updates)
SCAN_INTERVAL = timedelta(seconds=30)

# Keys for shared values in hass.data[DOMAIN]
_KEYS = {
    "storage_water_temp": "storage_water_temp",
    "current_power": "current_power",
    "current_water_temp": "current_water_temp",
    "current_outside_temp": "current_outside_temp",
    "current_heating_circuit_temp": "current_heating_circuit_temp",
    "current_operating_status": "current_operating_status",
    "current_heating_water_temp": "current_heating_water_temp",
    "current_status_heating": "current_status_heating",
    "current_status_hot_water": "current_status_hot_water",
}


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform (YAML)."""

    # Initialize shared dict if not present
    hass.data.setdefault(
        DOMAIN,
        {
            _KEYS["storage_water_temp"]: 0,
            _KEYS["current_power"]: 0,
            _KEYS["current_water_temp"]: 0,
            _KEYS["current_outside_temp"]: 0,
            _KEYS["current_heating_circuit_temp"]: 0,
            _KEYS["current_operating_status"]: None,
            _KEYS["current_heating_water_temp"]: 0,
            _KEYS["current_status_heating"]: None,
            _KEYS["current_status_hot_water"]: None,
        },
    )

    # Single reusable client
    client = RemkoHeatpump()
    hass.data[DOMAIN]["client"] = client

    add_entities(
        [
            RequestedWatertankTempSensor(hass, client),
            PowerConsumptionSensor(hass, client),
            CurrentWatertankTempSensor(hass, client),
            CurrentOutsideTemperatureSensor(hass, client),
            CurrentHeatingCircuitTemperatureSensor(hass, client),
            CurrentOperatingStatusSensor(hass, client),
            CurrentHeatingWaterTemperatureSensor(hass, client),
            CurrentStatusHeatingSensor(hass, client),
            CurrentStatusHotWaterSensor(hass, client),
        ],
        True,  # call update() before first state set
    )


class _BaseRemkoSensor(SensorEntity):
    """Base class for Remko sensors with shared helpers."""

    _attr_should_poll = True  # default, but explicit

    def __init__(self, hass: HomeAssistant, client: RemkoHeatpump) -> None:
        self.hass = hass
        self._client = client
        self._attr_native_value: Any = None  # filled in update()

    # convenience for setting and mirroring hass.data[DOMAIN] values
    def _set_shared(self, key: str, value: Any) -> None:
        self.hass.data[DOMAIN][key] = value
        self._attr_native_value = value


class RequestedWatertankTempSensor(_BaseRemkoSensor):
    _attr_name = "Remko Requested Watertank Temperature"
    _attr_icon = "mdi:thermometer-water"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_unique_id = "remko_requested_watertank_temperature"

    def update(self) -> None:
        try:
            hex_val = self._client.api_request(1082)
            value = int(hex_val, 16) / 10 if hex_val else None
            self._set_shared(_KEYS["storage_water_temp"], value)
        except Exception as e:  # noqa: BLE001
            _LOGGER.error("RequestedWatertankTempSensor error: %s", e)


class PowerConsumptionSensor(_BaseRemkoSensor):
    _attr_name = "Remko Power Consumption"
    _attr_icon = "mdi:lightning-bolt"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_unique_id = "remko_power_consumption"

    def update(self) -> None:
        try:
            hex_val = self._client.api_request(5320)
            value = int(hex_val, 16) * 100 if hex_val else None
            self._set_shared(_KEYS["current_power"], value)
        except Exception as e:  # noqa: BLE001
            _LOGGER.error("PowerConsumptionSensor error: %s", e)


class CurrentWatertankTempSensor(_BaseRemkoSensor):
    _attr_name = "Remko Current Watertank Temperature"
    _attr_icon = "mdi:thermometer-water"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_unique_id = "remko_current_watertank_temperature"

    def update(self) -> None:
        try:
            hex_val = self._client.api_request(5039)
            value = int(hex_val, 16) / 10 if hex_val else None
            self._set_shared(_KEYS["current_water_temp"], value)
        except Exception as e:  # noqa: BLE001
            _LOGGER.error("CurrentWatertankTempSensor error: %s", e)


class CurrentOutsideTemperatureSensor(_BaseRemkoSensor):
    _attr_name = "Remko Current Outside Temperature"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_unique_id = "remko_current_outside_temperature"

    def update(self) -> None:
        try:
            hex_val = self._client.api_request(5055)
            if not hex_val:
                self._set_shared(_KEYS["current_outside_temp"], None)
                return

            raw = int(hex_val, 16)
            # 16-bit signed (two's complement), scale 0.1
            signed = raw - 0x10000 if raw > 0x7FFF else raw
            value = signed / 10
            self._set_shared(_KEYS["current_outside_temp"], value)
        except Exception as e:  # noqa: BLE001
            _LOGGER.error("CurrentOutsideTemperatureSensor error: %s", e)


class CurrentHeatingCircuitTemperatureSensor(_BaseRemkoSensor):
    _attr_name = "Remko Current Heating Circuit Temperature"
    _attr_icon = "mdi:thermometer-check"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_unique_id = "remko_current_heating_circuit_temperature"

    def update(self) -> None:
        try:
            hex_val = self._client.api_request(5034)
            value = int(hex_val, 16) / 10 if hex_val else None
            self._set_shared(_KEYS["current_heating_circuit_temp"], value)
        except Exception as e:  # noqa: BLE001
            _LOGGER.error(
                "CurrentHeatingCircuitTemperatureSensor error: %s", e)


class CurrentOperatingStatusSensor(_BaseRemkoSensor):
    _attr_name = "Remko Current Operating Status"
    _attr_icon = "mdi:run"
    _attr_unique_id = "remko_current_operating_status"

    def update(self) -> None:
        try:
            code = self._client.api_request(5001)
            mapping = {
                "04": "Loading DHW",
                "0A": "Standby",
                "09": "Idle",
                "05": "Storage Energy",
                "06": "Heating",
                "07": "Cooling",
                "00": "Blocked",
                "40": "Ready",
                "0C": "Frost Protection",
                "02": "Defrosting",
                "03": "Loading defrost buffer",
            }
            value = mapping.get(code, f"Status N/A: {code}")
            self._set_shared(_KEYS["current_operating_status"], value)
        except Exception as e:  # noqa: BLE001
            _LOGGER.error("CurrentOperatingStatusSensor error: %s", e)


class CurrentHeatingWaterTemperatureSensor(_BaseRemkoSensor):
    _attr_name = "Remko Current Heating Water Temperature"
    _attr_icon = "mdi:thermometer-check"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_unique_id = "remko_current_heating_water_temperature"

    def update(self) -> None:
        try:
            hex_val = self._client.api_request(5190)
            value = int(hex_val, 16) / 10 if hex_val else None
            self._set_shared(_KEYS["current_heating_water_temp"], value)
        except Exception as e:  # noqa: BLE001
            _LOGGER.error("CurrentHeatingWaterTemperatureSensor error: %s", e)


class CurrentStatusHeatingSensor(_BaseRemkoSensor):
    _attr_name = "Remko Current Status Heating"
    _attr_icon = "mdi:heat-pump-outline"
    _attr_unique_id = "remko_current_status_heating"

    def update(self) -> None:
        try:
            code = self._client.api_request(1088)
            mapping = {
                "01": "Automatic",
                "02": "Heating",
                "03": "Standby",
                "04": "Cooling",
            }
            value = mapping.get(code, f"Heating Status N/A: ({code})")
            self._set_shared(_KEYS["current_status_heating"], value)
        except Exception as e:  # noqa: BLE001
            _LOGGER.error("CurrentStatusHeatingSensor error: %s", e)


class CurrentStatusHotWaterSensor(_BaseRemkoSensor):
    _attr_name = "Remko Current Status Hot Water"
    _attr_icon = "mdi:water"
    _attr_unique_id = "remko_current_status_hot_water"

    def update(self) -> None:
        try:
            code = self._client.api_request(1079)
            mapping = {
                "00": "Auto Comfort",
                "01": "Auto Eco",
                "02": "Solar / PV",
                "03": "Off",
            }
            value = mapping.get(code, f"Water Status N/A: ({code})")
            self._set_shared(_KEYS["current_status_hot_water"], value)
        except Exception as e:  # noqa: BLE001
            _LOGGER.error("CurrentStatusHotWaterSensor error: %s", e)
