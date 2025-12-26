"""Constants for the OpenRouter Fixed integration."""
from __future__ import annotations

DOMAIN = "open_router_fixed"
DEFAULT_NAME = "OpenRouter"
DEFAULT_API_URL = "https://openrouter.ai/api/v1"
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MODEL = "openai/gpt-3.5-turbo"

CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_MAX_TOKENS = "max_tokens"
CONF_TEMPERATURE = "temperature"
CONF_TOP_P = "top_p"
CONF_FREQUENCY_PENALTY = "frequency_penalty"
CONF_PRESENCE_PENALTY = "presence_penalty"

ATTR_MODEL = "model"
ATTR_MAX_TOKENS = "max_tokens"
ATTR_TEMPERATURE = "temperature"
ATTR_TOP_P = "top_p"
ATTR_FREQUENCY_PENALTY = "frequency_penalty"
ATTR_PRESENCE_PENALTY = "presence_penalty"

