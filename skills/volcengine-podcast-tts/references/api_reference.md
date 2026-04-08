# Volcengine Podcast TTS API Reference

This document provides detailed reference information for implementing the Volcengine Podcast TTS WebSocket protocol.

## WebSocket Endpoint

```
wss://openspeech.bytedance.com/api/v3/sami/podcasttts
```

## Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `X-Api-App-Id` | Your APP ID from Volcengine console | Yes |
| `X-Api-Access-Key` | Your Access Token from Volcengine console | Yes |
| `X-Api-Resource-Id` | `volc.service_type.10050` for Podcast TTS | Yes |
| `X-Api-App-Key` | Fixed value: `aGjiRDfUWi` | Yes |
| `X-Api-Connect-Id` | UUID for connection tracking | No |

## Binary Frame Format

All messages use a binary protocol with the following structure:

### Header (4 bytes)

| Byte | Bits | Description |
|------|------|-------------|
| 0 | 0-3 (left) | Protocol version: `0b0001` |
| 0 | 4-7 (right) | Header size: `0b0001` (4 bytes) |
| 1 | 0-3 (left) | Message type (see below) |
| 1 | 4-7 (right) | Message flags (see below) |
| 2 | 0-3 (left) | Serialization: `0b0001` (JSON) or `0b0000` (Raw) |
| 2 | 4-7 (right) | Compression: `0b0000` (none) or `0b0001` (gzip) |
| 3 | all | Reserved: `0x00` |

### Optional Fields (after header, before payload)

#### When flag is `WithEvent` (0b0100):

| Field | Size | Description |
|-------|------|-------------|
| Event | 4 bytes | Event number (int32, big-endian) |
| Session ID length | 4 bytes | Length of session ID (uint32, big-endian) |
| Session ID | variable | Session ID string (UTF-8) |

### Payload (after optional fields)

| Field | Size | Description |
|-------|------|-------------|
| Payload size | 4 bytes | Payload length (uint32, big-endian) |
| Payload | variable | Actual payload data |

## Message Types

| Type | Bits | Description |
|------|------|-------------|
| FullClientRequest | 0b0001 (1) | Full client request with event |
| AudioOnlyClient | 0b0010 (2) | Audio-only client message |
| FullServerResponse | 0b1001 (9) | Full server response |
| AudioOnlyServer | 0b1011 (11) | Audio-only server data |
| Error | 0b1111 (15) | Error response |

## Message Flags

| Flag | Bits | Description |
|------|------|-------------|
| NoSeq | 0b0000 (0) | No sequence |
| PositiveSeq | 0b0001 (1) | Positive sequence |
| LastNoSeq | 0b0010 (2) | Last packet, no sequence |
| NegativeSeq | 0b0011 (3) | Negative sequence |
| WithEvent | 0b0100 (4) | Payload contains event number |

## Event Types

### Connection Events (1-49)

| Event | Name | Description |
|-------|------|-------------|
| 1 | StartConnection | Start WebSocket connection |
| 2 | FinishConnection | End WebSocket connection |

### Connection Events (50-99)

| Event | Name | Description |
|-------|------|-------------|
| 50 | ConnectionStarted | Connection established |
| 51 | ConnectionFailed | Connection failed (auth error) |
| 52 | ConnectionFinished | Connection ended |

### Session Events (100-149)

| Event | Name | Description |
|-------|------|-------------|
| 100 | StartSession | Start podcast session |
| 101 | CancelSession | Cancel current session |
| 102 | FinishSession | End podcast session |

### Session Events (150-199)

| Event | Name | Description |
|-------|------|-------------|
| 150 | SessionStarted | Session started |
| 151 | SessionCanceled | Session canceled |
| 152 | SessionFinished | Session ended |
| 153 | SessionFailed | Session failed |
| 154 | UsageResponse | Token usage statistics |

### Podcast Events (350-399)

| Event | Name | Description |
|-------|------|-------------|
| 360 | PodcastRoundStart | New podcast round starts |
| 361 | PodcastRoundResponse | Audio data chunk |
| 362 | PodcastRoundEnd | Podcast round ends |
| 363 | PodcastEnd | All podcast content complete |

## Protocol Flow

```
Client                                    Server
  |                                         |
  |----- StartConnection (event=1) ------->|
  |                                         |
  |<---- ConnectionStarted (event=50) -----|
  |                                         |
  |----- StartSession (event=100) -------->|
  |     [JSON payload with text]          |
  |                                         |
  |<---- SessionStarted (event=150) -------|
  |                                         |
  |----- FinishSession (event=102) ------->|
  |                                         |
  |<---- PodcastRoundStart (event=360) ----|
  |     [Round info + speaker]             |
  |                                         |
  |<---- PodcastRoundResponse (event=361)-|
  |     [Audio chunk 1]                    |
  |                                         |
  |<---- PodcastRoundResponse (event=361)-|
  |     [Audio chunk 2]                    |
  |                                         |
  |<---- PodcastRoundEnd (event=362) ------|
  |                                         |
  |<---- PodcastRoundStart (event=360) ----|
  |     [Next round...]                    |
  |                                         |
  |<---- PodcastEnd (event=363) ----------|
  |     [Download URL]                     |
  |                                         |
  |<---- SessionFinished (event=152) -----|
  |                                         |
  |----- FinishConnection (event=2) ------>|
  |                                         |
  |<---- ConnectionFinished (event=52) ---|
  |                                         |
```

## Request Payload (JSON)

```json
{
  "input_id": "unique-request-id",
  "input_text": "要转换的文本内容",
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
    "speakers": [
      "zh_male_dayixiansheng_v2_saturn_bigtts",
      "zh_female_mizaitongxue_v2_saturn_bigtts"
    ]
  },
  "input_info": {
    "return_audio_url": true,
    "input_text_max_length": 12000
  }
}
```

### Payload Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_id` | string | required | Unique request identifier |
| `input_text` | string | - | Text to convert (max 32k chars) |
| `action` | int | 0 | 0=text summary, 3=NLP texts, 4=text expansion |
| `use_head_music` | bool | false | Add intro music |
| `use_tail_music` | bool | false | Add outro music |
| `audio_config.format` | string | mp3 | mp3, wav, ogg_opus, pcm, aac |
| `audio_config.sample_rate` | int | 24000 | 16000, 24000, 48000 |
| `audio_config.speech_rate` | int | 0 | -50 to 100, 0=normal |
| `speaker_info.random_order` | bool | true | Randomize speaker order |
| `speaker_info.speakers` | array | required | 2 speaker IDs |
| `input_info.return_audio_url` | bool | true | Return download URL |
| `input_info.input_text_max_length` | int | 12000 | Max chars for model (≤12000 recommended) |

## Available Speakers

### 黑猫侦探社咪仔 (Recommended)
- Male: `zh_male_dayixiansheng_v2_saturn_bigtts`
- Female: `zh_female_mizaitongxue_v2_saturn_bigtts`

### 刘飞和潇磊
- Male: `zh_male_liufei_v2_saturn_bigtts`
- Male: `zh_male_xiaolei_v2_saturn_bigtts`

## Response Events

### PodcastRoundStart (360)

```json
{
  "round_id": 0,
  "speaker": "zh_male_dayixiansheng_v2_saturn_bigtts",
  "text": "第一句话内容..."
}
```

### PodcastEnd (363)

```json
{
  "meta_info": {
    "audio_url": "https://...",
    "topics": null,
    "input_metrics": {
      "origin_input_text_length": 100,
      "input_text_length": 80,
      "input_text_truncated": false
    }
  }
}
```

### UsageResponse (154)

```json
{
  "usage": {
    "input_text_tokens": 980,
    "output_audio_tokens": 5000
  }
}
```

## SSL Configuration

The service uses a self-signed certificate. You may need to disable SSL verification:

```python
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

## Error Handling

### Error Response Frame

| Byte | Description |
|-----|-------------|
| 0 | Version (0b0001) \| Header Size (0b0001) |
| 1 | Message type (0b1111) \| Flags (0b0000) |
| 2 | Serialization (0b0001) \| Compression (0b0000) |
| 3 | Reserved |
| 4-7 | Error code (uint32, big-endian) |
| 8+ | Error message (JSON) |

### Common Error Codes

| Code | Description |
|------|-------------|
| Authentication failures | Invalid APP ID or Access Token |
| Certificate errors | SSL verification failed |
| Payload errors | Invalid JSON, missing fields |
| Rate limiting | Too many requests |
| Text too long | Input exceeds 32k characters |

## Best Practices

1. **Keep text under 12k characters** for best model performance
2. **Use speaker pairs from the same series** for best results
3. **Handle SSL verification** properly in production
4. **Set appropriate timeouts** for long-running podcast generation
5. **Implement retry logic** for network failures
6. **Use the download URL** when possible (more reliable than streaming)
