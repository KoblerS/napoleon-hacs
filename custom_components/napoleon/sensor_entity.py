"""Sensor entities for Napoleon Grill integration."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT, UnitOfTemperature
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import NapoleonDataCoordinator

PROBE_SENSORS = [
    ("PRB_TMP_ONE", "Probe 1 Temperature"),
    ("PRB_TMP_TWO", "Probe 2 Temperature"),
    ("PRB_TMP_THREE", "Probe 3 Temperature"),
    ("PRB_TMP_FOUR", "Probe 4 Temperature"),
]

SENSOR_DEFINITIONS = [
    *PROBE_SENSORS,
    ("BRT_LVL", "Brightness Level"),
    ("BT_LVL", "Burner Level"),
    ("RSSI", "WiFi Signal"),
    ("RST_CNT", "Reset Count"),
    ("PRB_STAT", "Probe Status"),
]

SENSOR_ICONS = {
    "PRB_TMP_ONE": "mdi:thermometer",
    "PRB_TMP_TWO": "mdi:thermometer",
    "PRB_TMP_THREE": "mdi:thermometer",
    "PRB_TMP_FOUR": "mdi:thermometer",
    "BRT_LVL": "mdi:brightness-6",
    "BT_LVL": "mdi:fire",
    "RSSI": "mdi:wifi",
    "RST_CNT": "mdi:restart",
    "PRB_STAT": "mdi:information-outline",
}


class NapoleonSensor(CoordinatorEntity, SensorEntity):
    """Sensor entity for a Napoleon grill property."""

    def __init__(
        self,
        coordinator: NapoleonDataCoordinator,
        entry: ConfigEntry,
        dsn: str,
        property_name: str,
        display_name: str,
        device_name: str,
    ) -> None:
        super().__init__(coordinator)
        self._dsn = dsn
        self._property_name = property_name
        self._attr_name = f"{device_name} {display_name}"
        self._attr_unique_id = f"napoleon_{dsn}_{property_name}"
        self._attr_icon = SENSOR_ICONS.get(property_name, "mdi:grill")

        if property_name in ("PRB_TMP_ONE", "PRB_TMP_TWO", "PRB_TMP_THREE", "PRB_TMP_FOUR"):
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif property_name == "RSSI":
            self._attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
            self._attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        device_data = data.get(self._dsn, {})
        properties = device_data.get("properties", {})
        return properties.get(self._property_name)

    @property
    def available(self) -> bool:
        data = self.coordinator.data or {}
        device_data = data.get(self._dsn, {})
        device = device_data.get("device", {})
        return device.get("connection_status") == "Online"


class NapoleonConnectionSensor(CoordinatorEntity, SensorEntity):
    """Sensor for device connection status."""

    def __init__(
        self,
        coordinator: NapoleonDataCoordinator,
        entry: ConfigEntry,
        dsn: str,
        device_name: str,
    ) -> None:
        super().__init__(coordinator)
        self._dsn = dsn
        self._attr_name = f"{device_name} Connection"
        self._attr_unique_id = f"napoleon_{dsn}_connection_status"
        self._attr_icon = "mdi:lan-connect"

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        device_data = data.get(self._dsn, {})
        device = device_data.get("device", {})
        return device.get("connection_status")


def create_napoleon_sensors(
    coordinator: NapoleonDataCoordinator, entry: ConfigEntry
) -> list[SensorEntity]:
    """Create sensor entities for all Napoleon devices."""
    sensors: list[SensorEntity] = []
    data = coordinator.data or {}

    for dsn, device_data in data.items():
        device = device_data.get("device", {})
        device_name = device.get("product_name", "Napoleon Grill")

        sensors.append(
            NapoleonConnectionSensor(coordinator, entry, dsn, device_name)
        )

        for property_name, display_name in SENSOR_DEFINITIONS:
            sensors.append(
                NapoleonSensor(
                    coordinator, entry, dsn, property_name, display_name, device_name
                )
            )

    return sensors
