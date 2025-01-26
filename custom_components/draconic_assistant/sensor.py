from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors from a config entry."""
    device_id = "draconic_reactor"

    # Create base sensors
    status_sensor = CustomSensor("Status", device_id, "Unknown")
    temperature_sensor = CustomSensor("Temperature", device_id, 0, unit_of_measurement="°C")
    saturation_sensor = CustomSensor("Saturation", device_id, 0)
    max_saturation_sensor = CustomSensor("Max Saturation", device_id, 0)
    field_strength_sensor = CustomSensor("Field Strength", device_id, 0)
    max_field_strength_sensor = CustomSensor("Max Field Strength", device_id, 0)
    field_drain_rate_sensor = CustomSensor("Field Drain Rate", device_id, 0, unit_of_measurement="RF/t")
    fuel_conversion_sensor = CustomSensor("Fuel Conversion", device_id, 0, unit_of_measurement="%")
    fuel_conversion_rate_sensor = CustomSensor("Fuel Conversion Rate", device_id, 0)
    failsafe_sensor = CustomSensor("Failsafe", device_id, 0)
    input_energy_sensor = CustomSensor("Input Energy", device_id, 0, unit_of_measurement="RF/t")
    output_energy_sensor = CustomSensor("Output Energy", device_id, 0, unit_of_measurement="RF/t")

    # Create calculated percentage sensors
    saturation_percentage_sensor = CalculatedSensor(
        "Saturation Percentage",
        device_id,
        saturation_sensor,
        max_saturation_sensor,
        unit_of_measurement="%",
    )
    field_strength_percentage_sensor = CalculatedSensor(
        "Field Strength Percentage",
        device_id,
        field_strength_sensor,
        max_field_strength_sensor,
        unit_of_measurement="%",
    )

    # Add all sensors to Home Assistant
    async_add_entities([
        status_sensor,
        temperature_sensor,
        saturation_sensor,
        max_saturation_sensor,
        saturation_percentage_sensor,
        field_strength_sensor,
        max_field_strength_sensor,
        field_strength_percentage_sensor,
        field_drain_rate_sensor,
        fuel_conversion_sensor,
        fuel_conversion_rate_sensor,
        failsafe_sensor,
        input_energy_sensor,
        output_energy_sensor,
    ], update_before_add=True)


class CustomSensor(SensorEntity):
    def __init__(self, name, device_id, state, unit_of_measurement=None):
        """Initialize a basic sensor."""
        self._attr_name = name
        self._attr_native_value = state
        self._attr_unit_of_measurement = unit_of_measurement
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_{name.lower().replace(' ', '_')}"


    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for grouping sensors under the same device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name="Draconic Reactor",
            manufacturer="YaBoiDan",
            model="1.0",
            sw_version="1.0",
        )

    async def async_update(self):
        """Optional: Update logic for this sensor if needed."""
        pass


class CalculatedSensor(SensorEntity):
    def __init__(self, name, device_id, base_sensor, max_sensor, unit_of_measurement=None):
        """Initialize a calculated sensor."""
        self._attr_name = name
        self._attr_native_value = None  # Start as None until calculated
        self._base_sensor = base_sensor
        self._max_sensor = max_sensor
        self._attr_unit_of_measurement = unit_of_measurement
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_{name.lower().replace(' ', '_')}"


    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for grouping sensors under the same device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name="Draconic Reactor",
            manufacturer="YaBoiDan",
            model="1.0",
            sw_version="1.0",
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
