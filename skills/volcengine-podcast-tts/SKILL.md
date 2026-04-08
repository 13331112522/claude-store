---
name: volcengine-podcast-tts
description: Use this skill when implementing Volcengine Podcast TTS API integration for generating podcast-style audio from text using WebSocket protocol. This skill provides the complete binary frame protocol implementation, message flow handling, and audio streaming logic.
---

# Volcengine Podcast TTS

## Overview

This skill enables implementation of Volcengine's Podcast TTS service, which generates podcast-style audio from Chinese text using dual-speaker dialogue. The service uses a custom WebSocket protocol with binary frame encoding.

## Quick Start

Use the provided protocol script when implementing Volcengine Podcast TTS:

```python
import asyncio
from scripts.volcengine_protocol import VolcenginePodcastTTS

async def main():
    client = VolcenginePodcastTTS(
        app_id="your_app_id",
        access_token="your_access_token"
    )

    audio_data, audio_url = await client.generate_podcast(
        text="要转换的文本内容",
        speakers=["zh_male_dayixiansheng_v2_saturn_bigtts",
                 "zh_female_mizaitongxue_v2_saturn_bigtts"]
    )

    with open("podcast.mp3", "wb") as f:
        f.write(audio_data)

asyncio.run(main())
```

## Protocol Implementation

### WebSocket Connection

The service uses a custom binary protocol over WebSocket. Key implementation details:

1. **SSL Verification**: Disable certificate verification (service uses self-signed cert)
2. **Headers**: Include `X-Api-App-Id`, `X-Api-Access-Key`, `X-Api-Resource-Id`, `X-Api-App-Key`
3. **websockets library**: Use `additional_headers` parameter (v16+), not `extra_headers`

### Binary Frame Structure

Messages use a 4-byte header with optional event/session fields:

```
Byte 0: Version (0b0001) | Header Size (0b0001)
Byte 1: Message Type (0b0001) | Flags (0b0100 for WithEvent)
Byte 2: Serialization (0b0001 for JSON) | Compression (0b0000)
Byte 3: Reserved (0x00)
```

When `WithEvent` flag is set:
- Bytes 4-7: Event number (int32, big-endian)
- Bytes 8-11: Session ID length (uint32, big-endian)
- Bytes 12+: Session ID (UTF-8)
- Then: Payload size (4 bytes) + Payload data

### Message Flow

Follow this exact sequence for successful podcast generation:

1. **StartConnection** (event=1) → Wait for **ConnectionStarted** (event=50)
2. **StartSession** (event=100) with payload → Wait for **SessionStarted** (event=150)
3. **FinishSession** (event=102)
4. Receive podcast data (events 360-363)
5. Wait for **SessionFinished** (event=152)
6. **FinishConnection** (event=2) → Wait for **ConnectionFinished** (event=52)

## Request Parameters

### Required Headers

| Header | Value |
|--------|-------|
| `X-Api-App-Id` | APP ID from Volcengine console |
| `X-Api-Access-Key` | Access Token from Volcengine console |
| `X-Api-Resource-Id` | `volc.service_type.10050` |
| `X-Api-App-Key` | `aGjiRDfUWi` (fixed value) |

### JSON Payload Structure

```json
{
  "input_id": "unique-id",
  "input_text": "文本内容",
  "action": 0,
  "use_head_music": false,
  "use_tail_music": false,
  "audio_config": {
    "format": "mp3",
    "sample_rate": 24000,
    "speech_rate": 0
  },
  "speaker_info": {
    "random_order": true,
    "speakers": ["speaker_a_id", "speaker_b_id"]
  },
  "input_info": {
    "return_audio_url": true,
    "input_text_max_length": 12000
  }
}
```

### Important Parameters

- **action**: 0 (text summary), 3 (NLP dialogue), 4 (text expansion)
- **input_text_max_length**: Keep ≤ 12000 for stable model performance (max 32000)
- **speakers**: Must use exactly 2 speakers from same series for best results

## Available Speakers

### 黑猫侦探社咪仔 (Recommended)
- `zh_male_dayixiansheng_v2_saturn_bigtts` (大一先生)
- `zh_female_mizaitongxue_v2_saturn_bigtts` (咪仔同学)

### 刘飞和潇磊
- `zh_male_liufei_v2_saturn_bigtts`
- `zh_male_xiaolei_v2_saturn_bigtts`

## Response Events

Handle these events during audio streaming:

| Event | Description |
|-------|-------------|
| 360 (PodcastRoundStart) | New dialogue round starts, includes speaker info |
| 361 (PodcastRoundResponse) | Audio data chunk (binary, add to buffer) |
| 362 (PodcastRoundEnd) | Current round ends |
| 363 (PodcastEnd) | Podcast complete, includes download URL |
| 152 (SessionFinished) | Session ends, close connection |
| 154 (UsageResponse) | Token usage statistics |

## Common Issues

### SSL Certificate Errors

The service uses a self-signed certificate. Disable verification:

```python
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

### Wrong Parameter Name

For websockets v16+, use `additional_headers` not `extra_headers`:

```python
# Correct
async with websockets.connect(url, additional_headers=headers) as ws:
    ...

# Incorrect (causes TypeError)
async with websockets.connect(url, extra_headers=headers) as ws:
    ...
```

### Authentication Failures

Verify:
- APP_ID and ACCESS_TOKEN are from correct Volcengine console
- Podcast TTS service is enabled (service ID: 10028)
- Credentials are not expired

### Connection Timeout

Podcast generation can take 30+ seconds for long text. Increase timeouts:

```python
async with websockets.connect(url, additional_headers=headers,
                                close_timeout=180, ping_timeout=180) as ws:
```

## Resources

### scripts/volcengine_protocol.py

Complete Python implementation of the Volcengine Podcast TTS WebSocket protocol. Provides:

- `VolcenginePodcastTTS` class for easy API interaction
- `build_message()` and `parse_message()` for frame encoding/decoding
- Enums for MsgType, MsgTypeFlagBits, and EventType
- Error handling for connection and session failures
- Progress callback support for real-time updates

Execute the script directly to read the implementation without loading into context, or read specific sections as needed.

### references/api_reference.md

Detailed API documentation including:
- Complete binary frame format specification
- All message types, flags, and event types
- Protocol flow diagram
- Request/response event formats
- Available speaker IDs
- Error handling and best practices

Load this reference when implementing the protocol from scratch or troubleshooting specific protocol issues.
