
from __future__ import annotations
from typing import Any, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfSpeed
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import WindDataCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator: WindDataCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        WindSpeedSensor(coordinator),
        WindGustsSensor(coordinator)
    ])

class WindBaseSensor(CoordinatorEntity[WindDataCoordinator], SensorEntity):
    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(self, coordinator: WindDataCoordinator) -> None:
        super().__init__(coordinator)

class WindSpeedSensor(WindBaseSensor):
    _attr_name = "Velocità vento"
    _attr_native_unit_of_measurement = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_icon = "mdi:weather-windy"
    _attr_unique_id = "guardia_vento_tende_wind_speed"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("wind_speed_kmh")

class WindGustsSensor(WindBaseSensor):
    _attr_name = "Raffiche vento"
    _attr_native_unit_of_measurement = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_icon = "mdi:weather-windy"
    _attr_unique_id = "guardia_vento_tende_wind_gusts"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("wind_gusts_kmh")
