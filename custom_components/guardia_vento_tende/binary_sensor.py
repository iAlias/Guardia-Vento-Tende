
from __future__ import annotations
from typing import Any
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    threshold = float(entry.options.get("threshold_kmh", entry.data.get("threshold_kmh", 35.0)))
    cycles_above = int(entry.options.get("cycles_above_to_trigger", entry.data.get("cycles_above_to_trigger", 2)))
    cycles_below = int(entry.options.get("cycles_below_to_clear", entry.data.get("cycles_below_to_clear", 2)))
    async_add_entities([AwningsWindAlertBinarySensor(coordinator, threshold, cycles_above, cycles_below)])

class AwningsWindAlertBinarySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Allerta vento tende"
    _attr_icon = "mdi:alarm-light"
    _attr_device_class = BinarySensorDeviceClass.SAFETY
    _attr_unique_id = "guardia_vento_tende_alert"

    def __init__(self, coordinator, threshold: float, cycles_above: int, cycles_below: int) -> None:
        super().__init__(coordinator)
        self._threshold = float(threshold)
        self._cycles_above_needed = max(1, int(cycles_above))
        self._cycles_below_needed = max(1, int(cycles_below))
        self._above_counter = 0
        self._below_counter = 0
        self._state_on = False

    @property
    def is_on(self) -> bool:
        return self._state_on

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        d = self.coordinator.data or {}
        return {
            "threshold_kmh": self._threshold,
            "wind_speed_kmh": d.get("wind_speed_kmh"),
            "wind_gusts_kmh": d.get("wind_gusts_kmh"),
            "last_update": d.get("time"),
            "cycles_above_to_trigger": self._cycles_above_needed,
            "cycles_below_to_clear": self._cycles_below_needed,
            "above_counter": self._above_counter,
            "below_counter": self._below_counter,
        }

    def _recompute_state(self) -> None:
        d = self.coordinator.data or {}
        speed = d.get("wind_speed_kmh")
        if speed is None:
            return
        if float(speed) >= self._threshold:
            self._above_counter += 1
            self._below_counter = 0
            if not self._state_on and self._above_counter >= self._cycles_above_needed:
                self._state_on = True
                _LOGGER.info("Allerta vento ATTIVA: %.1f km/h ≥ soglia %.1f per %d cicli", float(speed), self._threshold, self._cycles_above_needed)
        else:
            self._below_counter += 1
            self._above_counter = 0
            if self._state_on and self._below_counter >= self._cycles_below_needed:
                self._state_on = False
                _LOGGER.info("Allerta vento DISATTIVATA: %.1f km/h < soglia %.1f per %d cicli", float(speed), self._threshold, self._cycles_below_needed)

    def _handle_coordinator_update(self) -> None:
        self._recompute_state()
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.coordinator.async_add_listener(self._handle_coordinator_update))
