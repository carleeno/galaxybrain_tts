from unittest.mock import Mock, patch

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
import openai
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
import requests

from custom_components.galaxybrain_tts import async_setup_entry
from custom_components.galaxybrain_tts.const import (
    CONF_ELEVENLABS_API_KEY,
    CONF_MAX_TOKENS,
    CONF_MODEL,
    CONF_OPENAI_API_KEY,
    CONF_SIMILARITY,
    CONF_STABILITY,
    CONF_TEMPERATURE,
    CONF_TOP_P,
    CONF_VOICE,
    DOMAIN,
)
from custom_components.galaxybrain_tts.tts import GalaxyBrainProvider, get_engine


@pytest.fixture
def config() -> dict:
    return {
        CONF_OPENAI_API_KEY: "fake_api_key",
        CONF_ELEVENLABS_API_KEY: "fake_api_key2",
        CONF_VOICE: "John",
        CONF_STABILITY: 0.9,
        CONF_SIMILARITY: 0.5,
        CONF_MODEL: "gpt-3.5-turbo",
        CONF_MAX_TOKENS: 250,
        CONF_TEMPERATURE: 0.5,
        CONF_TOP_P: 0.5,
    }


@pytest.fixture
def config_entry(config: dict) -> ConfigEntry:
    return MockConfigEntry(domain="galaxybrain_tts", data=config)


@pytest.mark.asyncio
async def test_async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> None:
    """Test async_setup_entry function."""
    with patch(
        "custom_components.galaxybrain_tts.elevenlabs_client.ElevenLabsClient.get_voices"
    ), patch(
        "custom_components.galaxybrain_tts.elevenlabs_client.ElevenLabsClient.get_voice_by_name"
    ) as mock_get_voice, patch(
        "openai.Engine.list"
    ):
        mock_get_voice.return_value = {
            "voice_id": "fake_id",
            "name": "John",
        }
        # Call the async_setup_entry function
        result = await async_setup_entry(hass, config_entry)

        # Verify that the function returns the expected value
        assert result == True


@pytest.mark.asyncio
async def test_async_setup_entry_with_bad_api_key(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> None:
    """Test async_setup_entry function with bad API key."""
    # patch a 401
    with patch(
        "custom_components.galaxybrain_tts.elevenlabs_client.ElevenLabsClient.get_voices",
        side_effect=requests.exceptions.HTTPError(response=Mock(status_code=401)),
    ), patch("openai.Engine.list"):
        # Call the async_setup_entry function
        result = await async_setup_entry(hass, config_entry)

        # Verify that the function returns the expected value
        assert result == False


@pytest.mark.asyncio
async def test_async_setup_entry_with_bad_voice(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> None:
    """Test async_setup_entry function with bad voice."""
    with patch(
        "custom_components.galaxybrain_tts.elevenlabs_client.ElevenLabsClient.get_voices"
    ), patch("openai.Engine.list"):
        # Call the async_setup_entry function
        result = await async_setup_entry(hass, config_entry)

        # Verify that the function returns the expected value
        assert result == False


@pytest.mark.asyncio
async def test_async_setup_entry_with_exception(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> None:
    """Test async_setup_entry function with exception."""
    with patch(
        "custom_components.galaxybrain_tts.elevenlabs_client.ElevenLabsClient.get_voices",
        side_effect=Exception,
    ), patch("openai.Engine.list"):
        # ConfigEntryNotReady should be raised
        with pytest.raises(ConfigEntryNotReady):
            await async_setup_entry(hass, config_entry)


def test_elevenlabs_provider_init(hass: HomeAssistant, config: dict) -> None:
    """Test GalaxyBrainProvider init function."""
    with patch(
        "custom_components.galaxybrain_tts.elevenlabs_client.ElevenLabsClient.get_voices"
    ), patch("openai.Engine.list"):
        provider = get_engine(hass, config)

        assert isinstance(provider, GalaxyBrainProvider)
        assert provider.name == "GalaxyBrainTTS"
        assert provider.default_language == "en"
        assert provider.supported_languages == ["en"]


def test_elevenlabs_provider_get_tts_audio(hass: HomeAssistant, config: dict) -> None:
    """Test GalaxyBrainProvider get_tts_audio function."""
    with patch(
        "custom_components.galaxybrain_tts.elevenlabs_client.ElevenLabsClient"
    ) as mock_11l_client, patch("openai.Engine.list"), patch(
        "custom_components.galaxybrain_tts.openai_client.OpenAIClient.process"
    ):
        mock_11l_client.return_value.get_voices.return_value = None
        mock_11l_client.return_value.get_tts_audio.return_value = "mp3", b"fake_audio"

        # provider = get_engine(hass, config)

        # audio = provider.get_tts_audio("Hello", "en")

        # assert audio == ("mp3", b"fake_audio")
