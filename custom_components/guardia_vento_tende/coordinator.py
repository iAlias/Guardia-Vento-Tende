
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import OpenMeteoClient
from .const import (
    CONF_LAT, CONF_LON, CONF_SCAN_INTERVAL, CONF_USE_HOME_COORDS, DOMAIN,
    DEFAULT_LAT, DEFAULT_LON
)

_LOGGER = logging.getLogger(__name__)

class WindDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, lat: float, lon: float, scan_interval: int) -> None:
        self._client = OpenMeteoClient(async_get_clientsession(hass), lat, lon)
        super().__init__(
            hass,
            _LOGGER,
            name="Guardia Vento Tende",
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            data = await self._client.async_get_current()
            if data.get("wind_speed_kmh") is None:
                raise UpdateFailed("Dati vento non disponibili dalla fonte")
            return data
        except Exception as err:
            raise UpdateFailed(f"Errore aggiornamento dati: {err}") from err

async def create_coordinator(hass: HomeAssistant, entry: ConfigEntry) -> WindDataCoordinator:
    data = entry.data or {}
    options = entry.options or {}

    use_home = options.get(CONF_USE_HOME_COORDS, data.get(CONF_USE_HOME_COORDS, True))

    lat = (options.get(CONF_LAT) if not use_home else (hass.config.latitude or DEFAULT_LAT)) or DEFAULT_LAT
    lon = (options.get(CONF_LON) if not use_home else (hass.config.longitude or DEFAULT_LON)) or DEFAULT_LON

    scan_int = int(options.get(CONF_SCAN_INTERVAL, data.get(CONF_SCAN_INTERVAL, 300)))
    _LOGGER.debug("Coordinator setup lat=%s lon=%s scan_interval=%s", lat, lon, scan_int)

    coordinator = WindDataCoordinator(hass, float(lat), float(lon), scan_int)
    await coordinator.async_config_entry_first_refresh()
    return coordinator
