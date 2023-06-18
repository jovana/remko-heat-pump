"""Remko Sensor integration."""
# https://developers.home-assistant.io/docs/core/entity/sensor

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import TEMP_CELSIUS, POWER_KILO_WATT, POWER_WATT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import logging

from .const import DOMAIN
from .remko import RemkoHeatpump

_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.

    if discovery_info is None:
        return
    add_entities([
        RequestedWatertankTempSensor(),
        PowerConsumptionSensor(),
        CurrentWatertankTempSensor(),
        CurrentOutsideTemperatureSensor(),
        CurrentHeatingCircuitTemperatureSensor(),
        CurrentOperatingStatusSensor(),
        CurrentHeatingWaterTemperatureSensor(),
        CurrentStatusHeatingSensor(),
        CurrentStatusHotWaterSensor(),
    ])


class RequestedWatertankTempSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @ property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Remko Requested Watertank Temperature'

    @property
    def icon(self):
        return 'mdi:thermometer-water'

    @ property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @ property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            self.hass.data[DOMAIN]["storage_water_temp"] = int(
                RemkoHeatpump().api_request(1082), 16)/10
        except Exception as e:
            _LOGGER.error(
                f"An exception occurred in RequestedWatertankTempSensor: {e.__str__()}")
        self._state = self.hass.data[DOMAIN]['storage_water_temp']


class PowerConsumptionSensor(SensorEntity):
    """Representation of a sensor."""
    # _attr_device_class = SensorDeviceClass.POWER
    # _attr_name = "Example Temperature"
    # _attr_native_unit_of_measurement = TEMP_CELSIUS
    # _attr_device_class = SensorDeviceClass.TEMPERATURE
    # _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @ property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Remko Power Consumption'

    @ property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @ property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return POWER_WATT

    @property
    def icon(self):
        return 'mdi:lightning-bolt'

    @property
    def device_class(self):
        return SensorDeviceClass.POWER

    @property
    def state_class(self):
        return SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        try:
            self.hass.data[DOMAIN]["current_power"] = int(
                RemkoHeatpump().api_request(5320), 16)*100
        except Exception as e:
            _LOGGER.error(
                f"An exception occurred in PowerConsumptionSensor: {e.__str__()}")
        self._state = self.hass.data[DOMAIN]["current_power"]


class CurrentWatertankTempSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @ property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Remko Current Watertank Temperature'

    @property
    def icon(self):
        return 'mdi:thermometer-water'

    @ property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @ property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        try:
            self.hass.data[DOMAIN]["current_water_temp"] = int(
                RemkoHeatpump().api_request(5039), 16)/10
        except Exception as e:
            _LOGGER.error(
                f"An exception occurred in CurrentWatertankTempSensor: {e.__str__()}")

        self._state = self.hass.data[DOMAIN]["current_water_temp"]


class CurrentOutsideTemperatureSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @ property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Remko Current Outside Temperature'

    @ property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @ property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        try:
            self.hass.data[DOMAIN]["current_outside_temp"] = int(
                RemkoHeatpump().api_request(5055), 16)/10
        except Exception as e:
            _LOGGER.error(
                f"An exception occurred in CurrentOutsideTemperatureSensor: {e.__str__()}")
        self._state = self.hass.data[DOMAIN]["current_outside_temp"]


class CurrentHeatingCircuitTemperatureSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @ property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Remko Current Heating Circuit Temperature'

    @property
    def icon(self):
        return 'mdi:thermometer-check'

    @ property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @ property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        try:
            self.hass.data[DOMAIN]["current_heating_circuit_temp"] = int(
                RemkoHeatpump().api_request(5034), 16)/10
        except Exception as e:
            _LOGGER.error(
                f"An exception occurred in CurrentHeatingCircuitTemperatureSensor: {e.__str__()}")
        self._state = self.hass.data[DOMAIN]["current_heating_circuit_temp"]


class CurrentOperatingStatusSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @ property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Remko Current Operating Status'

    @ property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        return 'mdi:run'

    # @ property
    # def unit_of_measurement(self) -> str:
    #     """Return the unit of measurement."""
    #     return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        try:
            operation = RemkoHeatpump().api_request(5001)
            if operation == "04":
                self.hass.data[DOMAIN]["current_operating_status"] = "Loading DHW"
            elif operation == "0A":
                self.hass.data[DOMAIN]["current_operating_status"] = "Standby"
            elif operation == "09":
                self.hass.data[DOMAIN]["current_operating_status"] = "idle"
            elif operation == "06":
                self.hass.data[DOMAIN]["current_operating_status"] = "Heating"
            elif operation == "07":
                self.hass.data[DOMAIN]["current_operating_status"] = "Cooling"
            elif operation == "00":
                self.hass.data[DOMAIN]["current_operating_status"] = "Blocked"
            else:
                self.hass.data[DOMAIN]["current_operating_status"] = f"Status N/A: {operation}"
        except Exception as e:
            _LOGGER.error(
                f"An exception occurred in CurrentOperatingStatusSensor: {e.__str__()}")

        self._state = self.hass.data[DOMAIN]["current_operating_status"]


class CurrentHeatingWaterTemperatureSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @ property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Remko Current Heating Water Temperature'

    @property
    def icon(self):
        return 'mdi:thermometer-check'

    @ property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @ property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        try:
            self.hass.data[DOMAIN]["current_heating_water_temp"] = int(
                RemkoHeatpump().api_request(5190), 16)/10
        except Exception as e:
            _LOGGER.error(
                f"An exception occurred in CurrentHeatingWaterTemperatureSensor: {e.__str__()}")

        self._state = self.hass.data[DOMAIN]["current_heating_water_temp"]


class CurrentStatusHeatingSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @ property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Remko Current Status Heating'

    @property
    def icon(self):
        return 'mdi:heat-pump-outline'

    @ property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            operation = RemkoHeatpump().api_request(1088)
            if operation == "01":
                self.hass.data[DOMAIN]["current_status_heating"] = "Automatic"
            elif operation == "02":
                self.hass.data[DOMAIN]["current_status_heating"] = "Heating"
            elif operation == "03":
                self.hass.data[DOMAIN]["current_status_heating"] = "Standby"
            elif operation == "04":
                self.hass.data[DOMAIN]["current_status_heating"] = "Cooling"

            else:
                self.hass.data[DOMAIN]["current_status_heating"] = f"Status N/A: {operation}"

        except Exception as e:
            _LOGGER.error(
                f"An exception occurred in CurrentStatusHeatingSensor: {e.__str__()}")

        self._state = self.hass.data[DOMAIN]["current_status_heating"]


class CurrentStatusHotWaterSensor(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None

    @ property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'Remko Current Status Hot Water'

    @ property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        return 'mdi:water'

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        try:
            operation = RemkoHeatpump().api_request(1079)
            if operation == "00":
                self.hass.data[DOMAIN]["current_status_hot_water"] = "Auto Comfort"
            elif operation == "01":
                self.hass.data[DOMAIN]["current_status_hot_water"] = "Auto Eco"
            elif operation == "02":
                self.hass.data[DOMAIN]["current_status_hot_water"] = "Solar / PV"
            elif operation == "03":
                self.hass.data[DOMAIN]["current_status_hot_water"] = "Off"

            else:
                self.hass.data[DOMAIN]["current_status_hot_water"] = f"Status N/A: {operation}"
        except Exception as e:
            _LOGGER.error(
                f"An exception occurred in CurrentStatusHotWaterSensor: {e.__str__()}")

        self._state = self.hass.data[DOMAIN]["current_status_hot_water"]
