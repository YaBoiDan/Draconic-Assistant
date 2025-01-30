from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, DOMAIN_Pretty

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors from a config entry."""
    DOMAIN = "draconic_reactor"

    # Create base sensors
    status_sensor = CustomSensor("Status", DOMAIN, "Unknown")
    temperature_sensor = CustomSensor("Temperature", DOMAIN, 0, unit_of_measurement="°C")
    saturation_sensor = CustomSensor("Saturation", DOMAIN, 0)
    max_saturation_sensor = CustomSensor("Max Saturation", DOMAIN, 0)
    field_strength_sensor = CustomSensor("Field Strength", DOMAIN, 0)
    max_field_strength_sensor = CustomSensor("Max Field Strength", DOMAIN, 0)
    field_drain_rate_sensor = CustomSensor("Field Drain Rate", DOMAIN, 0, unit_of_measurement="RF/t")
    fuel_conversion_sensor = CustomSensor("Fuel Conversion", DOMAIN, 0, unit_of_measurement="%")
    fuel_conversion_rate_sensor = CustomSensor("Fuel Conversion Rate", DOMAIN, 0)
    failsafe_sensor = CustomSensor("Failsafe", DOMAIN, "false")
    input_energy_sensor = CustomSensor("Input Energy", DOMAIN, 0, unit_of_measurement="RF/t")
    output_energy_sensor = CustomSensor("Output Energy", DOMAIN, 0, unit_of_measurement="RF/t")

    # Create calculated percentage sensors
    CalculatedSensor(
        "Saturation Percentage",
        DOMAIN,
        saturation_sensor,
        max_saturation_sensor,
        unit_of_measurement="%",
    ),
    CalculatedSensor(
        "Field Strength Percentage",
        DOMAIN,
        field_strength_sensor,
        max_field_strength_sensor,
        unit_of_measurement="%",
    ),
    ]

    # Add all sensors to Home Assistant
    async_add_entities(sensors, update_before_add=True)


class CustomSensor(SensorEntity):
    def __init__(self, name, DOMAIN, state, unit_of_measurement=None):
        """Initialize a basic sensor."""
        self._attr_name = name
        self._device_id = DOMAIN
        self._sensor_name = DOMAIN_Pretty + " " + name
        self.entity_id = f"sensor.{DOMAIN}_{name}".lower()
        self._attr_native_value = state
        self._attr_unit_of_measurement = unit_of_measurement
        self._DOMAIN = DOMAIN
        self._attr_unique_id = f"{DOMAIN}_{name.lower().replace(' ', '_')}"

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
    def device_info(self) -> DeviceInfo:
        """Return device info for grouping sensors under the same device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._DOMAIN)},
            name="Draconic Reactor",
            manufacturer="YaBoiDan",
            model="1.0",
            sw_version="1.0",
        )

    async def async_update(self):
        """Optional: Update logic for this sensor if needed."""
        pass


class CalculatedSensor(SensorEntity):
    def __init__(self, name, DOMAIN, base_sensor, max_sensor, unit_of_measurement=None):
        """Initialize a calculated sensor."""
        self._attr_name = name
        self._device_id = DOMAIN
        self._sensor_name = DOMAIN_Pretty + " " + name
        self.entity_id = f"sensor.{DOMAIN}_{name}".lower()
        self._attr_native_value = None  # Start as None until calculated
        self._base_sensor = base_sensor
        self._max_sensor = max_sensor
        self._attr_unit_of_measurement = unit_of_measurement
        self._DOMAIN = DOMAIN
        self._attr_unique_id = f"{DOMAIN}_{name.lower().replace(' ', '_')}"

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
    def device_info(self) -> DeviceInfo:
        """Return device info for grouping sensors under the same device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._DOMAIN)},
            name="Draconic Reactor",
            manufacturer="YaBoiDan",
        )

    async def async_update(self):
        """Calculate percentage from the base and max sensors."""
        base_value = self._base_sensor.native_value
        max_value = self._max_sensor.native_value

        # Calculate the percentage, avoiding division by zero
        if max_value and max_value > 0:
            self._attr_native_value = (base_value / max_value) * 100
        else:
            self._attr_native_value = 0  # Graceful fallback
