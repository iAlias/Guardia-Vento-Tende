
from __future__ import annotations
from typing import Any
import aiohttp
import async_timeout
import logging

_LOGGER = logging.getLogger(__name__)

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&current=wind_speed_10m,wind_gusts_10m"
    "&windspeed_unit=kmh"
)

class OpenMeteoClient:
    def __init__(self, session: aiohttp.ClientSession, lat: float, lon: float) -> None:
        self._session = session
        self._lat = lat
        self._lon = lon

    async def async_get_current(self) -> dict[str, Any]:
        url = OPEN_METEO_URL.format(lat=self._lat, lon=self._lon)
        _LOGGER.debug("Fetching Open-Meteo: %s", url)
        async with async_timeout.timeout(15):
            async with self._session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()

        current = data.get("current", {})
        result = {
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "wind_gusts_kmh": current.get("wind_gusts_10m"),
            "time": current.get("time"),
            "lat": self._lat,
            "lon": self._lon,
        }
        _LOGGER.debug("Open-Meteo result: %s", result)
        return result
