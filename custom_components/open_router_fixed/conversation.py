"""Conversation agent for OpenRouter Fixed."""
from __future__ import annotations

import logging
from typing import Any

import httpx

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.util import ulid

from .const import DEFAULT_API_URL, DOMAIN
from .coordinator import OpenRouterCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up the conversation agent."""
    coordinator: OpenRouterCoordinator = hass.data[DOMAIN][entry.entry_id]

    conversation.async_set_agent(hass, entry, OpenRouterAgent(hass, coordinator))
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload the conversation agent."""
    conversation.async_unset_agent(hass, entry)
    return True


class OpenRouterAgent(conversation.AbstractConversationAgent):
    """OpenRouter conversation agent."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: OpenRouterCoordinator,
    ) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.coordinator = coordinator
        self.history: dict[str, list[dict[str, Any]]] = {}

    @property
    def attribution(self) -> dict[str, str]:
        """Return the attribution."""
        return {
            "name": "Powered by OpenRouter",
            "url": "https://openrouter.ai/",
        }

    @property
    def supported_languages(self) -> list[str] | str:
        """Return a list of supported languages."""
        return "*"

    @property
    def name(self) -> str:
        """Return the name of the agent."""
        return f"OpenRouter ({self.coordinator.model})"

    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        """Process a sentence."""
        conversation_id = user_input.conversation_id or ulid.ulid()
        conversation_context = self.history.get(conversation_id, [])

        # Add user message to history
        conversation_context.append({"role": "user", "content": user_input.text})

        # Prepare the request
        messages = conversation_context.copy()

        # Build request payload
        payload: dict[str, Any] = {
            "model": self.coordinator.model,
            "messages": messages,
            "max_tokens": self.coordinator.max_tokens,
            "temperature": self.coordinator.temperature,
        }

        # Add optional parameters if they exist
        if self.coordinator.top_p is not None:
            payload["top_p"] = self.coordinator.top_p
        if self.coordinator.frequency_penalty is not None:
            payload["frequency_penalty"] = self.coordinator.frequency_penalty
        if self.coordinator.presence_penalty is not None:
            payload["presence_penalty"] = self.coordinator.presence_penalty

        # Add Home Assistant context if available
        if user_input.context:
            system_message = self._build_system_message(user_input.context)
            if system_message:
                # Insert system message at the beginning
                messages_with_system = [system_message] + messages
                payload["messages"] = messages_with_system

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{DEFAULT_API_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.coordinator.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": f"{self.hass.config.api.base_url}",
                        "X-Title": "Home Assistant",
                    },
                    json=payload,
                    timeout=30.0,
                )
                response.raise_for_status()
                result = response.json()

        except httpx.HTTPStatusError as err:
            _LOGGER.error("OpenRouter API error: %s", err.response.text)
            intent_response = intent.IntentResponse()
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                f"Error communicating with OpenRouter: {err.response.status_code}",
            )
            return conversation.ConversationResult(
                response=intent_response, conversation_id=conversation_id
            )
        except httpx.RequestError as err:
            _LOGGER.error("Error connecting to OpenRouter: %s", err)
            intent_response = intent.IntentResponse()
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                "Error connecting to OpenRouter API",
            )
            return conversation.ConversationResult(
                response=intent_response, conversation_id=conversation_id
            )

        # Extract response
        if "choices" not in result or not result["choices"]:
            intent_response = intent.IntentResponse()
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                "No response from OpenRouter",
            )
            return conversation.ConversationResult(
                response=intent_response, conversation_id=conversation_id
            )

        assistant_message = result["choices"][0]["message"]["content"]

        # Add assistant response to history
        conversation_context.append({"role": "assistant", "content": assistant_message})
        self.history[conversation_id] = conversation_context

        # Limit history size to prevent excessive memory usage
        if len(conversation_context) > 20:
            # Keep first message (system if present) and last 19 messages
            if conversation_context[0].get("role") == "system":
                self.history[conversation_id] = (
                    [conversation_context[0]] + conversation_context[-19:]
                )
            else:
                self.history[conversation_id] = conversation_context[-20:]

        intent_response = intent.IntentResponse()
        intent_response.async_set_speech(assistant_message)
        return conversation.ConversationResult(
            response=intent_response, conversation_id=conversation_id
        )

    def _build_system_message(self, context: Any) -> dict[str, str] | None:
        """Build a system message with Home Assistant context."""
        try:
            # Get device information if available
            device_info = []
            if hasattr(context, "device_id") and context.device_id:
                device_info.append(f"Device ID: {context.device_id}")

            if device_info:
                return {
                    "role": "system",
                    "content": f"You are a helpful assistant integrated with Home Assistant. Context: {', '.join(device_info)}",
                }
        except Exception:  # pylint: disable=broad-except
            _LOGGER.debug("Could not build system message from context")
        return None

