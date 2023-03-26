DOMAIN = "galaxybrain_tts"
VERSION = "1.0.0"

CONF_ELEVENLABS_API_KEY = "11l_api_key"
CONF_VOICE = "voice"
DEFAULT_VOICE = "Domi"
CONF_STABILITY = "stability"
DEFAULT_STABILITY = 0.75
CONF_SIMILARITY = "similarity"
DEFAULT_SIMILARITY = 0.9

CONF_OPENAI_API_KEY = "oai_api_key"
CONF_MODEL = "model"
DEFAULT_MODEL = "gpt-3.5-turbo"
CONF_MAX_TOKENS = "max_tokens"
DEFAULT_MAX_TOKENS = 250
CONF_TEMPERATURE = "temperature"
DEFAULT_TEMPERATURE = 0.5
CONF_TOP_P = "top_p"
DEFAULT_TOP_P = 0.5

PRE_PROMPT = """You are a helpful and friendly Smart Home.

Your responses are synthesized to spoken words, avoid special characters or formatting that can not be spoken.
Prefer using full words over abbreviations (e.g. "Fahrenheit" instead of "F")

Follow the instructions below as a friendly, chatty home assistant.
"""
