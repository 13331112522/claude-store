#!/usr/bin/env python3
"""
Volcengine Podcast TTS WebSocket Protocol Implementation

This module provides a complete implementation of the Volcengine Podcast TTS
WebSocket protocol for generating podcast-style audio from text.

Usage:
    import asyncio
    from volcengine_protocol import VolcenginePodcastTTS

    async def main():
        client = VolcenginePodcastTTS(
            app_id="your_app_id",
            access_token="your_access_token",
            app_key="aGjiRDfUWi"
        )

        audio_data, audio_url = await client.generate_podcast(
            text="要转换的文本内容",
            speakers=["zh_male_dayixiansheng_v2_saturn_bigtts", "zh_female_mizaitongxue_v2_saturn_bigtts"],
            output_format="mp3"
        )

        # Save audio
        with open("podcast.mp3", "wb") as f:
            f.write(audio_data)

    asyncio.run(main())
"""

import asyncio
import ssl
import struct
import io
import json
import uuid
from enum import IntEnum
from typing import Optional, List, Tuple, Callable
import websockets


# Enums
class MsgType(IntEnum):
    """Message type enumeration for Volcengine WebSocket protocol"""
    Invalid = 0
    FullClientRequest = 0b0001
    AudioOnlyClient = 0b0010
    FullServerResponse = 0b1001
    AudioOnlyServer = 0b1011
    Error = 0b1111


class MsgTypeFlagBits(IntEnum):
    """Message type flag bits"""
    NoSeq = 0
    PositiveSeq = 0b0001
    LastNoSeq = 0b0010
    NegativeSeq = 0b0011
    WithEvent = 0b0100


class EventType(IntEnum):
    """Event type enumeration for Volcengine Podcast TTS"""
    None_ = 0
    # Connection events (1-49)
    StartConnection = 1
    FinishConnection = 2
    # Connection events (50-99)
    ConnectionStarted = 50
    ConnectionFailed = 51
    ConnectionFinished = 52
    # Session events (100-149)
    StartSession = 100
    CancelSession = 101
    FinishSession = 102
    # Session events (150-199)
    SessionStarted = 150
    SessionCanceled = 151
    SessionFinished = 152
    SessionFailed = 153
    UsageResponse = 154
    # Podcast events (350-399)
    PodcastRoundStart = 360
    PodcastRoundResponse = 361
    PodcastRoundEnd = 362
    PodcastEnd = 363


class ProtocolError(Exception):
    """Base exception for protocol errors"""
    pass


class ConnectionError(ProtocolError):
    """Connection failed"""
    pass


class SessionError(ProtocolError):
    """Session failed"""
    pass


def build_message(msg_type: MsgType, flag: MsgTypeFlagBits, event: EventType = EventType.None_,
                  session_id: str = "", payload: bytes = b"") -> bytes:
    """
    Build a binary message according to Volcengine WebSocket protocol.

    Args:
        msg_type: Message type (FullClientRequest, AudioOnlyClient, etc.)
        flag: Message type flag (WithEvent, NoSeq, etc.)
        event: Event type (for messages with WithEvent flag)
        session_id: Session ID (for session events)
        payload: Message payload

    Returns:
        Binary message bytes
    """
    buffer = io.BytesIO()

    # Write 4-byte header
    buffer.write(bytes([
        (1 << 4) | 1,  # Version 1, Header Size 4
        (msg_type << 4) | flag,  # Message Type | Flags
        (1 << 4) | 0,  # JSON serialization, no compression
        0,  # Reserved
    ]))

    # Write event if flag is WithEvent
    if flag == MsgTypeFlagBits.WithEvent:
        buffer.write(struct.pack(">i", event))

        # Write session_id for session events (not connection events)
        if event not in [EventType.StartConnection, EventType.FinishConnection,
                        EventType.ConnectionStarted, EventType.ConnectionFailed,
                        EventType.ConnectionFinished]:
            session_bytes = session_id.encode("utf-8")
            buffer.write(struct.pack(">I", len(session_bytes)))
            if session_bytes:
                buffer.write(session_bytes)

    # Write payload
    buffer.write(struct.pack(">I", len(payload)))
    if payload:
        buffer.write(payload)

    return buffer.getvalue()


def parse_message(data: bytes) -> dict:
    """
    Parse a binary message from Volcengine WebSocket server.

    Args:
        data: Binary message bytes

    Returns:
        Dictionary with parsed message fields:
        - msg_type: Message type enum
        - flag: Message flag enum
        - event: Event type enum
        - session_id: Session ID (if applicable)
        - payload: Message payload bytes
    """
    if isinstance(data, str):
        raise ValueError(f"Unexpected text message: {data}")

    buffer = io.BytesIO(data)

    # Read header
    byte0 = buffer.read(1)[0]
    byte1 = buffer.read(1)[0]
    byte2 = buffer.read(1)[0]
    byte3 = buffer.read(1)[0]

    msg_type = MsgType(byte1 >> 4)
    flag = MsgTypeFlagBits(byte1 & 0x0F)
    serialization = (byte2 >> 4) & 0x0F
    compression = byte2 & 0x0F

    event = EventType.None_
    session_id = ""
    payload = b""

    # Read event and session_id if flag is WithEvent
    if flag == MsgTypeFlagBits.WithEvent:
        event_bytes = buffer.read(4)
        if event_bytes:
            event = EventType(struct.unpack(">i", event_bytes)[0])

        # Read session_id for session events
        if event not in [EventType.StartConnection, EventType.FinishConnection,
                        EventType.ConnectionStarted, EventType.ConnectionFailed,
                        EventType.ConnectionFinished]:
            size_bytes = buffer.read(4)
            if size_bytes:
                size = struct.unpack(">I", size_bytes)[0]
                if size > 0:
                    session_id = buffer.read(size).decode("utf-8")

    # Read connect_id for connection events
    if event in [EventType.ConnectionStarted, EventType.ConnectionFailed,
                 EventType.ConnectionFinished]:
        size_bytes = buffer.read(4)
        if size_bytes:
            size = struct.unpack(">I", size_bytes)[0]
            if size > 0:
                buffer.read(size)  # Skip connect_id

    # Read payload
    size_bytes = buffer.read(4)
    if size_bytes:
        size = struct.unpack(">I", size_bytes)[0]
        if size > 0:
            payload = buffer.read(size)

    return {
        'msg_type': msg_type,
        'flag': flag,
        'event': event,
        'session_id': session_id,
        'payload': payload
    }


class VolcenginePodcastTTS:
    """
    Volcengine Podcast TTS WebSocket client.

    This class handles the complete WebSocket protocol flow for generating
    podcast-style audio from text using Volcengine's TTS service.
    """

    DEFAULT_ENDPOINT = "wss://openspeech.bytedance.com/api/v3/sami/podcasttts"
    DEFAULT_APP_KEY = "aGjiRDfUWi"

    def __init__(self, app_id: str, access_token: str, app_key: str = DEFAULT_APP_KEY,
                 endpoint: str = DEFAULT_ENDPOINT):
        """
        Initialize the Volcengine Podcast TTS client.

        Args:
            app_id: Volcengine APP ID
            access_token: Volcengine Access Token
            app_key: Volcengine App Key (default: "aGjiRDfUWi")
            endpoint: WebSocket endpoint URL
        """
        self.app_id = app_id
        self.access_token = access_token
        self.app_key = app_key
        self.endpoint = endpoint

    async def _get_headers(self) -> dict:
        """Get WebSocket connection headers"""
        return {
            "X-Api-App-Id": self.app_id,
            "X-Api-Access-Key": self.access_token,
            "X-Api-Resource-Id": "volc.service_type.10050",
            "X-Api-App-Key": self.app_key,
            "X-Api-Connect-Id": str(uuid.uuid4()),
        }

    async def _send_message(self, ws, msg_type: MsgType, flag: MsgTypeFlagBits,
                           event: EventType = EventType.None_, session_id: str = "",
                           payload: bytes = b""):
        """Send a message to the WebSocket server"""
        frame = build_message(msg_type, flag, event, session_id, payload)
        await ws.send(frame)

    async def _receive_message(self, ws):
        """Receive and parse a message from the WebSocket server"""
        data = await ws.recv()
        return parse_message(data)

    async def _wait_for_event(self, ws, expected_event: EventType):
        """Wait for a specific event type"""
        while True:
            msg = await self._receive_message(ws)

            if msg['event'] == expected_event:
                return msg

            if msg['event'] == EventType.ConnectionFailed:
                raise ConnectionError(msg['payload'].decode('utf-8', errors='ignore'))

            if msg['event'] == EventType.SessionFailed:
                raise SessionError(msg['payload'].decode('utf-8', errors='ignore'))

            if msg['msg_type'] == MsgType.Error:
                error_code = struct.unpack('>I', msg['payload'][:4])[0] if len(msg['payload']) >= 4 else 0
                error_msg = msg['payload'][4:].decode('utf-8', errors='ignore')
                raise ProtocolError(f"Error {error_code}: {error_msg}")

    def _build_request_payload(self, text: str, speakers: List[str],
                               use_head_music: bool = False,
                               use_tail_music: bool = False,
                               output_format: str = "mp3",
                               sample_rate: int = 24000,
                               speech_rate: int = 0,
                               return_audio_url: bool = True,
                               max_text_length: int = 12000) -> dict:
        """Build the request payload for StartSession"""
        return {
            "input_id": str(uuid.uuid4()),
            "input_text": text,
            "action": 0,
            "use_head_music": use_head_music,
            "use_tail_music": use_tail_music,
            "audio_config": {
                "format": output_format,
                "sample_rate": sample_rate,
                "speech_rate": speech_rate
            },
            "speaker_info": {
                "random_order": True,
                "speakers": speakers
            },
            "input_info": {
                "return_audio_url": return_audio_url,
                "input_text_max_length": max_text_length
            }
        }

    async def generate_podcast(
        self,
        text: str,
        speakers: Optional[List[str]] = None,
        use_head_music: bool = False,
        use_tail_music: bool = False,
        output_format: str = "mp3",
        sample_rate: int = 24000,
        speech_rate: int = 0,
        return_audio_url: bool = True,
        max_text_length: int = 12000,
        progress_callback: Optional[Callable] = None
    ) -> Tuple[bytes, Optional[str]]:
        """
        Generate a podcast from text using Volcengine TTS service.

        Args:
            text: Input text to convert to podcast
            speakers: List of speaker IDs (default: dayixiansheng and mizaitongxue)
            use_head_music: Whether to use head music
            use_tail_music: Whether to use tail music
            output_format: Audio format (mp3, wav, ogg_opus, pcm, aac)
            sample_rate: Audio sample rate (16000, 24000, 48000)
            speech_rate: Speech rate adjustment (-50 to 100, 0 is normal)
            return_audio_url: Whether to request a download URL
            max_text_length: Maximum text length for model processing
            progress_callback: Optional callback function for progress updates

        Returns:
            Tuple of (audio_data bytes, audio_url str or None)

        Raises:
            ConnectionError: If WebSocket connection fails
            SessionError: If session creation fails
            ProtocolError: For other protocol errors
        """
        if speakers is None:
            speakers = [
                "zh_male_dayixiansheng_v2_saturn_bigtts",
                "zh_female_mizaitongxue_v2_saturn_bigtts"
            ]

        # Truncate text if too long (API limit is 32k)
        if len(text) > 32000:
            text = text[:32000]

        headers = await self._get_headers()
        payload = self._build_request_payload(
            text=text,
            speakers=speakers,
            use_head_music=use_head_music,
            use_tail_music=use_tail_music,
            output_format=output_format,
            sample_rate=sample_rate,
            speech_rate=speech_rate,
            return_audio_url=return_audio_url,
            max_text_length=max_text_length
        )

        audio_data = b""
        audio_url = None
        session_id = str(uuid.uuid4())

        # Create SSL context that skips verification (for compatibility)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with websockets.connect(self.endpoint, additional_headers=headers,
                                     ssl=ssl_context) as ws:
            # 1. Start connection
            await self._send_message(ws, MsgType.FullClientRequest, MsgTypeFlagBits.WithEvent,
                                     EventType.StartConnection, payload=b'{}')

            # 2. Wait for ConnectionStarted
            await self._wait_for_event(ws, EventType.ConnectionStarted)

            # 3. Start session with payload
            payload_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            await self._send_message(ws, MsgType.FullClientRequest, MsgTypeFlagBits.WithEvent,
                                     EventType.StartSession, session_id, payload_bytes)

            # 4. Wait for SessionStarted
            await self._wait_for_event(ws, EventType.SessionStarted)

            # 5. Finish session
            await self._send_message(ws, MsgType.FullClientRequest, MsgTypeFlagBits.WithEvent,
                                     EventType.FinishSession, session_id, payload=b'{}')

            # 6. Receive podcast data
            while True:
                msg = await self._receive_message(ws)

                if progress_callback and msg['event'] in [
                    EventType.PodcastRoundStart,
                    EventType.PodcastRoundResponse,
                    EventType.PodcastRoundEnd,
                    EventType.PodcastEnd,
                    EventType.UsageResponse
                ]:
                    await progress_callback(msg)

                # Audio data
                if msg['event'] == EventType.PodcastRoundResponse:
                    audio_data += msg['payload']

                # Podcast end with download URL
                elif msg['event'] == EventType.PodcastEnd and msg['payload']:
                    data = json.loads(msg['payload'].decode('utf-8'))
                    meta_info = data.get("meta_info", {})
                    audio_url = meta_info.get("audio_url")

                # Session finished
                elif msg['event'] == EventType.SessionFinished:
                    break

            # 7. Finish connection
            await self._send_message(ws, MsgType.FullClientRequest, MsgTypeFlagBits.WithEvent,
                                     EventType.FinishConnection, payload=b'{}')

            # 8. Wait for ConnectionFinished
            await self._wait_for_event(ws, EventType.ConnectionFinished)

        return audio_data, audio_url


# Convenience function
async def generate_podcast(
    text: str,
    app_id: str,
    access_token: str,
    app_key: str = "aGjiRDfUWi",
    speakers: Optional[List[str]] = None,
    output_format: str = "mp3"
) -> Tuple[bytes, Optional[str]]:
    """
    Convenience function to generate a podcast from text.

    Args:
        text: Input text
        app_id: Volcengine APP ID
        access_token: Volcengine Access Token
        app_key: Volcengine App Key
        speakers: List of speaker IDs
        output_format: Audio format

    Returns:
        Tuple of (audio_data bytes, audio_url str or None)
    """
    client = VolcenginePodcastTTS(app_id, access_token, app_key)
    return await client.generate_podcast(text, speakers=speakers, output_format=output_format)
