"""Data coordinator for Napoleon Grill integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ApiError, NapoleonAylaApi
from .const import CONF_EMAIL, CONF_PASSWORD, CONF_REGION, DEFAULT_REGION

_LOGGER = logging.getLogger(__name__)


class NapoleonDataCoordinator(DataUpdateCoordinator):
    """Coordinator to poll Napoleon grill data from the Ayla API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.api = NapoleonAylaApi(
            entry.data[CONF_EMAIL],
            entry.data[CONF_PASSWORD],
            entry.data.get(CONF_REGION, DEFAULT_REGION),
        )
        self.api.set_tokens(
            entry.data["access_token"], entry.data["refresh_token"]
        )

        super().__init__(
            hass,
            _LOGGER,
            name="Napoleon Grill",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from the Ayla API."""
        try:
            devices = await self.api.get_devices()
            result = {}

            for device_entry in devices:
                device = device_entry.get("device", {})
                dsn = device.get("dsn")
                if not dsn:
                    continue

                properties = await self.api.get_device_properties(dsn)
                props_map = {}
                for prop_entry in properties:
                    prop = prop_entry.get("property", {})
                    name = prop.get("name")
                    if name:
                        props_map[name] = prop.get("value")

                result[dsn] = {
                    "device": device,
                    "properties": props_map,
                }

            return result
        except ApiError as err:
            raise UpdateFailed(f"API error: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err
