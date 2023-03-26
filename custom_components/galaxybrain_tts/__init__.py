"""GalaxyBrain TTS Custom Integration"""
from functools import partial
import logging

from homeassistant import core
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
import openai
from openai.error import AuthenticationError, OpenAIError
import requests

from .const import CONF_OPENAI_API_KEY, CONF_VOICE, DEFAULT_VOICE
from .elevenlabs_client import ElevenLabsClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: core.HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the ElevenLabs TTS component from a config entry."""
    voice_name = entry.data.get(CONF_VOICE, DEFAULT_VOICE)
    client = ElevenLabsClient(entry.data)
    openai.api_key = entry.data.get(CONF_OPENAI_API_KEY)

    try:
        await hass.async_add_executor_job(client.get_voices)
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            _LOGGER.error("Invalid ElevenLabs API key")
            return False
        raise ConfigEntryNotReady from err
    except Exception as err:
        raise ConfigEntryNotReady from err
    try:
        await hass.async_add_executor_job(
            partial(openai.Engine.list, request_timeout=10)
        )
    except AuthenticationError as err:
        _LOGGER.error("Invalid OpenAI API key: %s", err)
        return False
    except OpenAIError as err:
        raise ConfigEntryNotReady(err) from err

    voice = client.get_voice_by_name(voice_name)
    if not voice:
        _LOGGER.error("Invalid voice name")
        return False

    return True


async def async_unload_entry(hass: core.HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload OpenAI."""
    openai.api_key = None
    return True
