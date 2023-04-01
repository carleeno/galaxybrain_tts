import logging
from time import sleep

import openai
from openai.error import OpenAIError

from .const import (
    CONF_MAX_TOKENS,
    CONF_MODEL,
    CONF_OPENAI_API_KEY,
    CONF_TEMPERATURE,
    CONF_TOP_P,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    PRE_PROMPT,
)

_LOGGER = logging.getLogger(__name__)


class OpenAIClient:
    """OpenAI API client."""

    def __init__(self, config: dict) -> None:
        """Initialize the client."""
        self.config = config
        openai.api_key = config.get(CONF_OPENAI_API_KEY)

    def process(self, prompt: str, options: dict | None = None) -> str:
        """Process a prompt with the OpenAI API."""
        _LOGGER.debug("Processing prompt: %s", prompt)
        if options is None:
            options = {}
        model = options.get(CONF_MODEL, self.config.get(CONF_MODEL, DEFAULT_MODEL))
        max_tokens = options.get(
            CONF_MAX_TOKENS, self.config.get(CONF_MAX_TOKENS, DEFAULT_MAX_TOKENS)
        )
        temperature = options.get(
            CONF_TEMPERATURE, self.config.get(CONF_TEMPERATURE, DEFAULT_TEMPERATURE)
        )
        top_p = options.get(CONF_TOP_P, self.config.get(CONF_TOP_P, DEFAULT_TOP_P))
        tries = 0
        while tries < 3:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": PRE_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=int(max_tokens),
                    top_p=float(top_p),
                    temperature=float(temperature),
                )
                return response["choices"][0]["message"]["content"].strip()
            except OpenAIError as err:
                _LOGGER.warning("Error processing prompt: %s", err)
                tries += 1
                sleep(tries * 2)

        _LOGGER.error("Error processing prompt after 3 attempts")
        return "Sorry, I had a problem talking to OpenAI."
