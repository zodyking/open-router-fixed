"""Config flow for OpenRouter Fixed integration."""
from __future__ import annotations

import logging
from typing import Any

import httpx
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_FREQUENCY_PENALTY,
    CONF_MAX_TOKENS,
    CONF_MODEL,
    CONF_PRESENCE_PENALTY,
    CONF_TEMPERATURE,
    CONF_TOP_P,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
    }
)


async def validate_api_key(hass: HomeAssistant, api_key: str) -> None:
    """Validate the API key by making a test request."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10.0,
        )
        if response.status_code == 401:
            raise InvalidAuth
        response.raise_for_status()


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenRouter Fixed."""

    VERSION = 1

    @staticmethod
    async def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            await validate_api_key(self.hass, user_input[CONF_API_KEY])
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except httpx.HTTPError:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            # Store only API key in data, defaults will be used
            return self.async_create_entry(
                title="OpenRouter",
                data={CONF_API_KEY: user_input[CONF_API_KEY]},
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_import(self, config: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(config)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for OpenRouter Fixed."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current options or use defaults
        options = self.options or {}
        entry_data = self.config_entry.data
        
        # Helper to get value with proper None handling
        def get_value(key: str, default: Any = None) -> Any:
            if key in options:
                return options[key]
            if key in entry_data:
                return entry_data[key]
            return default
        
        # Use options first, then entry_data, then defaults
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_MODEL,
                    default=get_value(CONF_MODEL, DEFAULT_MODEL)
                ): str,
                vol.Required(
                    CONF_MAX_TOKENS,
                    default=get_value(CONF_MAX_TOKENS, DEFAULT_MAX_TOKENS),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=32000)),
                vol.Optional(
                    CONF_TEMPERATURE,
                    default=get_value(CONF_TEMPERATURE, DEFAULT_TEMPERATURE),
                ): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=2.0)),
                vol.Optional(
                    CONF_TOP_P,
                    default=get_value(CONF_TOP_P)
                ): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=1.0)),
                vol.Optional(
                    CONF_FREQUENCY_PENALTY,
                    default=get_value(CONF_FREQUENCY_PENALTY)
                ): vol.All(vol.Coerce(float), vol.Range(min=-2.0, max=2.0)),
                vol.Optional(
                    CONF_PRESENCE_PENALTY,
                    default=get_value(CONF_PRESENCE_PENALTY)
                ): vol.All(vol.Coerce(float), vol.Range(min=-2.0, max=2.0)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

