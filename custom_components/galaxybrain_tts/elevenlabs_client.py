import logging

import requests

from .const import (
    CONF_ELEVENLABS_API_KEY,
    CONF_SIMILARITY,
    CONF_STABILITY,
    CONF_VOICE,
    DEFAULT_SIMILARITY,
    DEFAULT_STABILITY,
    DEFAULT_VOICE,
)

_LOGGER = logging.getLogger(__name__)


class ElevenLabsClient:
    """A class to handle the connection to the ElevenLabs API."""

    def __init__(self, config: dict) -> None:
        """Initialize the client."""
        _LOGGER.debug("Initializing ElevenLabs client")
        self._11l_url = "https://api.elevenlabs.io/v1"
        self._headers = {"Content-Type": "application/json"}
        if config.get(CONF_ELEVENLABS_API_KEY):
            self._headers["xi-api-key"] = config[CONF_ELEVENLABS_API_KEY]

        # [{"voice_id": str, "name": str, ...}]
        self._voices: list[dict] = []
        self.config = config

    def get_voices(self) -> list:
        self._voices = []
        url = f"{self._11l_url}/voices"
        _LOGGER.debug("Fetching voices from %s", url)
        response = requests.get(url, headers=self._headers)
        _LOGGER.debug("Response status: %s", response.status_code)
        if not response.ok:
            raise requests.exceptions.HTTPError(response=response)
        self._voices = (response.json())["voices"]
        _LOGGER.debug("Found %s voices", len(self._voices))
        return self._voices

    def get_voice_by_name(self, name: str) -> dict:
        """Get a voice by its name."""
        _LOGGER.debug("Looking for voice with name %s", name)
        for voice in self._voices:
            if voice["name"] == name:
                _LOGGER.debug("Found voice %s from name %s", voice["voice_id"], name)
                return voice
        _LOGGER.warning("Could not find voice with name %s", name)
        return {}

    def get_tts_audio(self, message: str, options: dict | None = None) -> bytes:
        voice_id, stability, similarity = self.get_tts_options(options)
        url = f"{self._11l_url}/text-to-speech/{voice_id}"
        data = {
            "text": message,
            "voice_settings": {"stability": stability, "similarity_boost": similarity},
        }

        _LOGGER.debug("Requesting TTS from %s", url)
        _LOGGER.debug("Request data: %s", data)

        response = requests.post(url, headers=self._headers, json=data)
        _LOGGER.debug("Response status: %s", response.status_code)
        if not response.ok:
            raise requests.exceptions.HTTPError(response=response)
        return "mp3", response.content

    def get_tts_options(self, options: dict) -> tuple[str, float, float]:
        if not options:
            options = {}
        voice = options.get(CONF_VOICE, self.config.get(CONF_VOICE, DEFAULT_VOICE))
        stability = options.get(
            CONF_STABILITY, self.config.get(CONF_STABILITY, DEFAULT_STABILITY)
        )
        similarity = options.get(
            CONF_SIMILARITY, self.config.get(CONF_SIMILARITY, DEFAULT_SIMILARITY)
        )

        if not self._voices:
            _LOGGER.debug("No voices found, fetching them now")
            self.get_voices()

        if not self._voices:
            _LOGGER.error("No voices available, returning empty audio")
            return b""

        voice_id = self.get_voice_by_name(voice).get("voice_id", None)
        if not voice_id:
            _LOGGER.warning("Could not find voice with name %s", voice)
            voice_id = self._voices[0]["voice_id"]

        return voice_id, stability, similarity