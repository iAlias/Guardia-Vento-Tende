
from __future__ import annotations

DOMAIN = "guardia_vento_tende"

CONF_THRESHOLD = "threshold_kmh"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_USE_HOME_COORDS = "use_home_coordinates"
CONF_LAT = "latitude"
CONF_LON = "longitude"
CONF_CYCLES_ABOVE = "cycles_above_to_trigger"
CONF_CYCLES_BELOW = "cycles_below_to_clear"

DEFAULT_THRESHOLD = 35.0
DEFAULT_SCAN_INTERVAL = 300  # seconds
DEFAULT_CYCLES_ABOVE = 2
DEFAULT_CYCLES_BELOW = 2

SERVICE_REFRESH = "aggiorna_dati"
