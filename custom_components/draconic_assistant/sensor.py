from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors from a config entry."""
    device_id = "draconic_reactor"

    # Create base sensors
    sensors = [
    CustomSensor("Status", device_id, "Unknown"),
    CustomSensor("Temperature", device_id, 0, unit_of_measurement="°C"),
    CustomSensor("Saturation", device_id, 0),
    CustomSensor("Max Saturation", device_id, 0),
    CustomSensor("Field Strength", device_id, 0),
    CustomSensor("Max Field Strength", device_id, 0),
    CustomSensor("Field Drain Rate", device_id, 0, unit_of_measurement="RF/t"),
    CustomSensor("Fuel Conversion", device_id, 0, unit_of_measurement="%"),
    CustomSensor("Fuel Conversion Rate", device_id, 0),
    CustomSensor("Failsafe", device_id, "false"),
    CustomSensor("Input Energy", device_id, 0, unit_of_measurement="RF/t"),
    CustomSensor("Output Energy", device_id, 0, unit_of_measurement="RF/t"),

    # Create calculated percentage sensors
    CalculatedSensor(
        "Saturation Percentage",
        device_id,
        base_sensor=CustomSensor("Saturation", device_id, 0),
        max_sensor=CustomSensor("Max Saturation", device_id, 0),
        unit_of_measurement="%",
    ),
    CalculatedSensor(
        "Field Strength Percentage",
        device_id,
        base_sensor=CustomSensor("Field Strength", device_id, 0, unit_of_measurement="RF/t"),
        max_sensor=CustomSensor("Max Field Strength", device_id, 0, unit_of_measurement="RF/t"),
        unit_of_measurement="%",
    ),
    ]

    # Add all sensors to Home Assistant
    async_add_entities(sensors, update_before_add=True)


class CustomSensor(SensorEntity):
    def __init__(self, name, device_id, state, unit_of_measurement=None):
        """Initialize a basic sensor."""
        self._device_id = device_id
        self._sensor_name = name  # Display name (e.g., "Failsafe")
        self._attr_native_value = state
        self._attr_unit_of_measurement = unit_of_measurement
        # Ensure unique_id includes the device name
        self._attr_unique_id = f"{device_id}_{name.lower().replace(' ', '_')}"

    @property
    def name(self):
        """Return the display name of the sensor."""
        return self._sensor_name  # Display name: "Failsafe", "Temperature", etc.

    @property
    def device_info(self):
        """Return device info to group entities under the same device."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": "Draconic Reactor",
            "manufacturer": "YaboiDan",
            "model": "1.0",
            "sw_version": "1.0",
        }

    @property
    def entity_id(self):
        """Return the entity ID."""
        return f"sensor.{self._device_id}_{self._sensor_name.lower().replace(' ', '_')}"

    async def async_update(self):
        """Optional: Update logic for this sensor if needed."""
        pass


class CalculatedSensor(SensorEntity):
    def __init__(self, name, device_id, base_sensor, max_sensor, unit_of_measurement=None):
        """Initialize a calculated sensor."""
        self._device_id = device_id
        self._sensor_name = name  # Display name (e.g., "Field Strength Percentage")
        self._attr_native_value = None
        self._base_sensor = base_sensor
        self._max_sensor = max_sensor
        self._attr_unit_of_measurement = unit_of_measurement
        # Ensure unique_id includes the device name
        self._attr_unique_id = f"{device_id}_{name.lower().replace(' ', '_')}"

    @property
    def name(self):
        """Return the display name of the sensor."""
        return self._sensor_name  # Display name: "Field Strength Percentage"

    @property
    def device_info(self):
        """Return device info to group entities under the same device."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": "Draconic Reactor",
            "manufacturer": "YaboiDan",
            "model": "1.0",
            "sw_version": "1.0",
        }

    @property
    def entity_id(self):
        """Return the entity ID."""
        return f"sensor.{self._device_id}_{self._sensor_name.lower().replace(' ', '_')}"

    async def async_update(self):
        """Calculate percentage from the base and max sensors."""
        base_value = self._base_sensor.native_value
        max_value = self._max_sensor.native_value

        if max_value and max_value > 0:
            self._attr_native_value = (base_value / max_value) * 100
        else:
            self._attr_native_value = 0


    async def async_update(self):
        """Calculate percentage from the base and max sensors."""
        base_value = self._base_sensor.native_value
        max_value = self._max_sensor.native_value

        # Calculate the percentage, avoiding division by zero
        if max_value and max_value > 0:
            self._attr_native_value = (base_value / max_value) * 100
        else:
            self._attr_native_value = 0  # Graceful fallback
