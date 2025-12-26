"""DataUpdateCoordinator for OpenRouter Fixed."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_API_KEY,
    CONF_FREQUENCY_PENALTY,
    CONF_MAX_TOKENS,
    CONF_MODEL,
    CONF_PRESENCE_PENALTY,
    CONF_TEMPERATURE,
    CONF_TOP_P,
    DOMAIN,
)


class OpenRouterCoordinator(DataUpdateCoordinator):
    """Coordinator for OpenRouter Fixed."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=__import__("logging").getLogger(__name__),
            name=DOMAIN,
        )
        self.entry = entry
        self._update_from_entry()

    def _update_from_entry(self) -> None:
        """Update configuration from entry data and options."""
        from .const import (
            DEFAULT_MAX_TOKENS,
            DEFAULT_MODEL,
            DEFAULT_TEMPERATURE,
        )
        
        # Options override entry data, which override defaults
        options = self.entry.options or {}
        data = self.entry.data

        # Helper to get value with proper None handling
        def get_value(key: str, default: Any = None) -> Any:
            if key in options:
                return options[key]
            if key in data:
                return data[key]
            return default

        self.api_key = data[CONF_API_KEY]
        self.model = get_value(CONF_MODEL, DEFAULT_MODEL)
        self.max_tokens = get_value(CONF_MAX_TOKENS, DEFAULT_MAX_TOKENS)
        self.temperature = get_value(CONF_TEMPERATURE, DEFAULT_TEMPERATURE)
        self.top_p = get_value(CONF_TOP_P)
        self.frequency_penalty = get_value(CONF_FREQUENCY_PENALTY)
        self.presence_penalty = get_value(CONF_PRESENCE_PENALTY)

    async def _async_update_data(self) -> dict:
        """Fetch data from OpenRouter."""
        # This coordinator doesn't need to poll data,
        # but we keep it for consistency with HA patterns
        return {}

