from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo

DOMAIN = "draconic_reactor"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    # Create a device and its entities
    device_id = "draconic_reactor"
    entities = [
        CustomSensor("Status", device_id, "Unknown"),
        CustomSensor("Temperature", device_id, 0, unit_of_measurement="°C"),
        CustomSensor("Saturation", device_id, 0),
        CustomSensor("Max Saturation", device_id, 0),
        #CustomSensor("Saturation Percentage", device_id, 0, unit_of_measurement="%"),
        CustomSensor("Field Strength", device_id, 0),
        CustomSensor("Max Field Strength", device_id, 0),
        # CustomSensor("Field Strength Percentage", device_id, 0, unit_of_measurement="%"),
        CustomSensor("Field Drain Rate", device_id, 0),
        CustomSensor("Fuel Conversion", device_id, 0, unit_of_measurement="%"),
        CustomSensor("Fuel Conversion Rate", device_id, 0),
        CustomSensor("Field Drain Rate", device_id, 0),
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
