
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN, CONF_THRESHOLD, CONF_SCAN_INTERVAL, CONF_USE_HOME_COORDS,
    CONF_LAT, CONF_LON, CONF_CYCLES_ABOVE, CONF_CYCLES_BELOW,
    DEFAULT_THRESHOLD, DEFAULT_SCAN_INTERVAL, DEFAULT_CYCLES_ABOVE, DEFAULT_CYCLES_BELOW
)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Optional(CONF_THRESHOLD, default=DEFAULT_THRESHOLD): vol.Coerce(float),
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.Coerce(int),
    vol.Optional(CONF_USE_HOME_COORDS, default=True): bool,
    vol.Optional(CONF_LAT): vol.Coerce(float),
    vol.Optional(CONF_LON): vol.Coerce(float),
    vol.Optional(CONF_CYCLES_ABOVE, default=DEFAULT_CYCLES_ABOVE): vol.Coerce(int),
    vol.Optional(CONF_CYCLES_BELOW, default=DEFAULT_CYCLES_BELOW): vol.Coerce(int),
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="Guardia Vento Tende", data=user_input)
        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

    async def async_step_import(self, user_input=None) -> FlowResult:
        return await self.async_step_user(user_input)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        return await self.async_step_options(user_input)

    async def async_step_options(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data = self.config_entry.data
        opts = self.config_entry.options
        schema = vol.Schema({
            vol.Optional(CONF_THRESHOLD, default=opts.get(CONF_THRESHOLD, data.get(CONF_THRESHOLD, DEFAULT_THRESHOLD))): vol.Coerce(float),
            vol.Optional(CONF_SCAN_INTERVAL, default=opts.get(CONF_SCAN_INTERVAL, data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))): vol.Coerce(int),
            vol.Optional(CONF_USE_HOME_COORDS, default=opts.get(CONF_USE_HOME_COORDS, data.get(CONF_USE_HOME_COORDS, True))): bool,
            vol.Optional(CONF_LAT, default=opts.get(CONF_LAT, data.get(CONF_LAT))): vol.Optional(vol.Coerce(float)),
            vol.Optional(CONF_LON, default=opts.get(CONF_LON, data.get(CONF_LON))): vol.Optional(vol.Coerce(float)),
            vol.Optional(CONF_CYCLES_ABOVE, default=opts.get(CONF_CYCLES_ABOVE, data.get(CONF_CYCLES_ABOVE, DEFAULT_CYCLES_ABOVE))): vol.Coerce(int),
            vol.Optional(CONF_CYCLES_BELOW, default=opts.get(CONF_CYCLES_BELOW, data.get(CONF_CYCLES_BELOW, DEFAULT_CYCLES_BELOW))): vol.Coerce(int),
        })
        return self.async_show_form(step_id="options", data_schema=schema)

async def async_get_options_flow(config_entry):
    return OptionsFlowHandler(config_entry)
