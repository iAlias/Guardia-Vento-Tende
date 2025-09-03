
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
    CONF_LAT, CONF_LON, CONF_SCAN_INTERVAL, CONF_USE_HOME_COORDS, DOMAIN
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
            return data
        except Exception as err:
            raise UpdateFailed(str(err)) from err

async def create_coordinator(hass: HomeAssistant, entry: ConfigEntry) -> WindDataCoordinator:
    data = entry.data
    options = entry.options

    use_home = options.get("use_home_coordinates", data.get("use_home_coordinates", True))

    lat = (options.get("latitude") if not use_home else hass.config.latitude) or hass.config.latitude
    lon = (options.get("longitude") if not use_home else hass.config.longitude) or hass.config.longitude

    scan_int = int(options.get("scan_interval", data.get("scan_interval", 300)))
    _LOGGER.debug("Coordinator setup lat=%s lon=%s scan_interval=%s", lat, lon, scan_int)

    coordinator = WindDataCoordinator(hass, float(lat), float(lon), scan_int)
    await coordinator.async_config_entry_first_refresh()
    return coordinator
