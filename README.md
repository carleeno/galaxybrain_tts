# GalaxyBrain TTS for Home Assistant

This integration allows you to use OpenAI and ElevenLabs APIs as a text-to-speech provider for Home Assistant.

It's party trick is that your message is passed through chatGPT before sent to TTS, so you can transform complex sensor data into nice textual information via prompt engineering.

Disclaimer: This repo, the code within, and the maintainer/owner of this repo are in no way affiliated with OpenAI or ElevenLabs.

Privacy disclaimer: Data is transmitted to both OpenAI and elevenlabs.io when using this TTS service, do not use it for text containing sensitive information.

You can find OpenAI's privacy policy [here](https://openai.com/policies/privacy-policy)
You can find ElevenLab's privacy policy [here](https://beta.elevenlabs.io/privacy)

## Installation

This component is available via HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories) which is the recommended method of installation.

You can also copy `custom_components/galaxybrain_tts` to your `custom_components` folder in HomeAssistant if you prefer to install manually.

## Example `tts` entry in your `configuration.yaml`

```yaml
tts:
  - platform: galaxybrain_tts
    oai_api_key: !secret openai_api_key
    11l_api_key: !secret elevenlabs_api_key
    voice: Domi
    stability: 0.75
    similarity: 0.75
    model: gpt-3.5-turbo
    temperature: 0.5
    top_p: 0.5
    max_tokens: 250
```

### Options:

- `platform` - specifies to use this component, must be `galaxybrain_tts`
- `oai_api_key` - your OpenAI api key (sk-...), required.
- `11l_api_key` - (optional) get access to your own ElevenLab account's voices
- `voice` - (optional, default: Domi) use a different voice
- `stability` - (optional, default: 0.75) set the stability of the speech synthesis
- `similarity` - (optional, default: 0.75) set the clarity/similarity boost of the speech synthesis
- `model` - (optional, default: gpt-3.5-turbo) specify an alternative chat model (completion models not supported)
- `temperature` - (optional, default: 0.5) adjust the model's temperature setting
- `top_p` - (optional, default: 0.5) adjust the model's top_p setting
- `max_tokens` - (optional, default: 250) the max size of the response from the model

See [here](https://platform.openai.com/docs/api-reference/chat/create) for a description of the OpenAI parameters.

## API keys

An OpenAI API key is required, but can be obtained for free by creating an account at platform.openai.com. It's recommended to adjust your max budget to prevent unexpected and expensive overages.

At the time of writing, it's possible to use this without an ElevenLabs API key, but don't expect it to work for long.

To get an ElevenLabs API key, create an account at elevenlabs.io, and go to Profile Settings to copy it.

Note that using this extension will count against your API quotas for both services. As such, **DO NOT** use this TTS service for critical announcements, it will stop working once you've used up your quota.

## Caching

This integration inherently uses caching for the responses, meaning that if the text and options are the same as a previous service call, the response audio likely will be a replay of the previous response. The downside is this negates the natural variability you'd expect when repeating the same input data. The upside is that it reduces your quota usage and speeds up responses.

Note that passing in volatile data into the message (such as the current time) means that you will never see cached results, as the message is never the same.

## Example service call

```yaml
service: tts.galaxybrain_tts_say
data:
  options:
    voice: Bella
    temperature: 0.9
  entity_id: media_player.bedroom_speaker
  message: >
    The time is {{now()}}, the weather is:

    {{ expand('weather.dark_sky') }}

    The user just woke up, greet the user and provide a short summary of
    today's weather, include anything notable.

    Then state the date and share an interesting tidbit about today or today's
    history.
```

The parameters in `options` are fully optional, this allows you to override any options defined in `configuration.yaml` except for the api keys.
