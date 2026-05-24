"""Sensor platform for Napoleon Grill integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import NapoleonDataCoordinator
from .sensor_entity import create_napoleon_sensors


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Napoleon Grill sensors from a config entry."""
    coordinator = NapoleonDataCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities(create_napoleon_sensors(coordinator, entry))
