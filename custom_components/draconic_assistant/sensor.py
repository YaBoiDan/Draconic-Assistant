from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo

DOMAIN = "draconic_reactor"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    # Create a device and its entities
    device_id = "draconic_reactor"

    # Create the base sensors
    field_strength_sensor = CustomSensor("Field Strength", device_id, 0)
    max_field_strength_sensor = CustomSensor("Max Field Strength", device_id, 0)
    saturation_sensor = CustomSensor("Saturation", device_id, 0)
    max_saturation_sensor = CustomSensor("Max Saturation", device_id, 0)

    # Create the calculated percentage sensors
    saturation_percentage_sensor = CalculatedSensor(
        "Saturation Percentage",
        device_id,
        saturation_sensor,
        max_saturation_sensor,
        "%",
    )
    field_strength_percentage_sensor = CalculatedSensor(
        "Field Strength Percentage",
        device_id,
        field_strength_sensor,
        max_field_strength_sensor,
        "%",
    )

    # Add all sensors to Home Assistant
    entities = [
        CustomSensor("Status", device_id, "Unknown"),
        CustomSensor("Temperature", device_id, 0, unit_of_measurement="°C"),
        saturation_sensor,
        max_saturation_sensor,
        field_strength_sensor,
        max_field_strength_sensor,
        saturation_percentage_sensor,
        field_strength_percentage_sensor,
        CustomSensor("Field Drain Rate", device_id, 0),
        CustomSensor("Fuel Conversion", device_id, 0, unit_of_measurement="%"),
        CustomSensor("Fuel Conversion Rate", device_id, 0),
        CustomSensor("Failsafe", device_id, 0),
        CustomSensor("Input Energy", device_id, 0, unit_of_measurement="RF/t"),
        CustomSensor("Output Energy", device_id, 0, unit_of_measurement="RF/t"),
    ]

    async_add_entities(entities, update_before_add=True)


class CustomSensor(SensorEntity):
    def __init__(self, name, device_id, state, unit_of_measurement=None):
        self._attr_name = name
        self._attr_native_value = state
        self._attr_unit_of_measurement = unit_of_measurement
        self._device_id = device_id

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name="Draconic Reactor",
            manufacturer="YaBoiDan",
            model="1.0",
            sw_version="1.0",
        )

    async def async_update(self):
        # This method can be used to fetch updated data if needed.
        pass


class CalculatedSensor(SensorEntity):
    def __init__(self, name, device_id, base_sensor, max_sensor, unit_of_measurement=None):
        self._attr_name = name
        self._attr_native_value = None  # Start as None until calculated
        self._base_sensor = base_sensor
        self._max_sensor = max_sensor
        self._attr_unit_of_measurement = unit_of_measurement
        self._device_id = device_id

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name="Draconic Reactor",
            manufacturer="YaBoiDan",
            model="1.0",
            sw_version="1.0",
        )

    async def async_update(self):
        # Fetch values from the base and max sensors
        base_value = self._base_sensor.native_value
        max_value = self._max_sensor.native_value

        # Calculate the percentage, avoiding division by zero
        if max_value and max_value > 0:
            self._attr_native_value = (base_value / max_value) * 100
        else:
            self._attr_native_value = 0  # Graceful fallback
