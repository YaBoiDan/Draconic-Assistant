from homeassistant import config_entries
from .const import DOMAIN

class DraconicReactorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Draconic Reactor integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Create the config entry if the user submitted the form
            return self.async_create_entry(title="Draconic Reactor", data=user_input)

        # Show a configuration form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})  # Add any user inputs you'd like to collect
        )
