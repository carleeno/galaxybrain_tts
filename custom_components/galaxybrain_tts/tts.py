import logging

from homeassistant import core
from homeassistant.components.tts import Provider, TtsAudioType

from .const import (
    CONF_SIMILARITY,
    CONF_STABILITY,
    CONF_VOICE,
    CONF_VOICE_MODEL,
    CONF_OPTIMIZE_LATENCY,
    CONF_MODEL,
    CONF_MAX_TOKENS,
    CONF_TEMPERATURE,
    CONF_TOP_P,
)
from .elevenlabs_client import ElevenLabsClient
from .openai_client import OpenAIClient

_LOGGER = logging.getLogger(__name__)


def get_engine(hass: core.HomeAssistant, config: dict, discovery_info=None) -> Provider:
    """Set up ElevenLabs TTS component."""
    elevenlabs_client = ElevenLabsClient(config)
    openai_client = OpenAIClient(config)

    return GalaxyBrainProvider(openai_client, elevenlabs_client)


class GalaxyBrainProvider(Provider):
    """The ElevenLabs TTS API provider."""

    def __init__(
        self, openai_client: OpenAIClient, elevenlabs_client: ElevenLabsClient
    ) -> None:
        """Initialize the provider."""
        self._openai_client = openai_client
        self._11l_client = elevenlabs_client
        self._name = "GalaxyBrainTTS"

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return "en"

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return ["en"]

    @property
    def supported_options(self) -> list[str]:
        """Return list of supported options."""
        return [
            CONF_VOICE,
            CONF_STABILITY,
            CONF_SIMILARITY,
            CONF_VOICE_MODEL,
            CONF_OPTIMIZE_LATENCY,
            CONF_MODEL,
            CONF_MAX_TOKENS,
            CONF_TEMPERATURE,
            CONF_TOP_P,
        ]

    def get_tts_audio(
        self, message: str, language: str, options: dict | None = None
    ) -> TtsAudioType:
        """Load TTS from the ElevenLabs API."""
        message = self._openai_client.process(message, options)
        return self._11l_client.get_tts_audio(message, options)

    @property
    def name(self) -> str:
        """Return provider name."""
        return self._name

    @property
    def extra_state_attributes(self) -> dict:
        """Return provider attributes."""
        return {"provider": self._name}
