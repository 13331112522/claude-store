#!/usr/bin/env python3
"""
火山引擎 Podcast TTS 播客生成脚本
用法: python3 volc_podcast.py <文本内容> [输出文件名]
"""

import sys
import json
import uuid
import asyncio
import websockets
import argparse
import ssl
import struct
import io
from enum import IntEnum

# 配置
APP_ID = "4243287022"
ACCESS_TOKEN = "i2MarDfvjlf0Piv7Zwudu3dt2htyVJr4"
SECRET_KEY = "G1n8DekRMJ-idmr-2bDpoiKS9twV0iqo"
WS_URL = "wss://openspeech.bytedance.com/api/v3/sami/podcasttts"

# 发音人选项
SPEAKERS = [
    "zh_male_dayixiansheng_v2_saturn_bigtts",  # 大一先生
    "zh_female_mizaitongxue_v2_saturn_bigtts", # 咪仔同学
]

# Enums from official protocols.py
class MsgType(IntEnum):
    Invalid = 0
    FullClientRequest = 0b0001
    AudioOnlyClient = 0b0010
    FullServerResponse = 0b1001
    AudioOnlyServer = 0b1011
    Error = 0b1111

class MsgTypeFlagBits(IntEnum):
    NoSeq = 0
    PositiveSeq = 0b0001
    LastNoSeq = 0b0010
    NegativeSeq = 0b0011
    WithEvent = 0b0100

class EventType(IntEnum):
    None_ = 0
    StartConnection = 1
    FinishConnection = 2
    ConnectionStarted = 50
    ConnectionFailed = 51
    ConnectionFinished = 52
    StartSession = 100
    CancelSession = 101
    FinishSession = 102
    SessionStarted = 150
    SessionCanceled = 151
    SessionFinished = 152
    SessionFailed = 153
    UsageResponse = 154
    PodcastRoundStart = 360
    PodcastRoundResponse = 361
    PodcastRoundEnd = 362
    PodcastEnd = 363

def build_message(msg_type: MsgType, flag: MsgTypeFlagBits, event: EventType = EventType.None_,
                  session_id: str = "", payload: bytes = b"") -> bytes:
    """构建符合协议的二进制消息"""
    buffer = io.BytesIO()

    # Write header (4 bytes)
    buffer.write(bytes([
        (1 << 4) | 1,  # Version 1, Header Size 4 (4 bytes)
        (msg_type << 4) | flag,  # Message Type | Flags
        (1 << 4) | 0,  # JSON serialization, no compression
        0,  # Reserved
    ]))

    # Write event if flag is WithEvent
    if flag == MsgTypeFlagBits.WithEvent:
        buffer.write(struct.pack(">i", event))

        # Write session_id (except for connection events)
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

async def send_message(ws, msg_type: MsgType, flag: MsgTypeFlagBits, event: EventType = EventType.None_,
                       session_id: str = "", payload: bytes = b""):
    """发送消息到WebSocket"""
    frame = build_message(msg_type, flag, event, session_id, payload)
    print(f"发送: MsgType={msg_type.name}, Flag={flag.name}, Event={event.name}, SessionID={session_id[:8] if session_id else 'N/A'}")
    await ws.send(frame)

async def receive_message(ws):
    """从WebSocket接收消息"""
    data = await ws.recv()
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

        # Read session_id
        if event not in [EventType.StartConnection, EventType.FinishConnection,
                        EventType.ConnectionStarted, EventType.ConnectionFailed,
                        EventType.ConnectionFinished]:
            size_bytes = buffer.read(4)
            if size_bytes:
                size = struct.unpack(">I", size_bytes)[0]
                if size > 0:
                    session_id = buffer.read(size).decode("utf-8")

    # Read connect_id for connection events
    if event in [EventType.ConnectionStarted, EventType.ConnectionFailed, EventType.ConnectionFinished]:
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

    print(f"接收: MsgType={msg_type.name}, Event={event.name}, PayloadSize={len(payload)}")

    return {
        'msg_type': msg_type,
        'flag': flag,
        'event': event,
        'session_id': session_id,
        'payload': payload
    }

async def wait_for_event(ws, expected_event: EventType):
    """等待特定事件"""
    while True:
        msg = await receive_message(ws)
        if msg['event'] == expected_event:
            return msg
        if msg['event'] == EventType.ConnectionFailed:
            raise RuntimeError(f"Connection failed: {msg['payload'].decode('utf-8', errors='ignore')}")
        if msg['msg_type'] == MsgType.Error:
            raise RuntimeError(f"Server error: {msg['payload'].decode('utf-8', errors='ignore')}")

async def generate_podcast(text: str, output_file: str = "podcast.mp3"):
    """生成播客音频"""

    headers = {
        "X-Api-App-Id": APP_ID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": "volc.service_type.10050",
        "X-Api-App-Key": "aGjiRDfUWi",
        "X-Api-Connect-Id": str(uuid.uuid4()),
    }

    payload = {
        "input_id": str(uuid.uuid4()),
        "input_text": text,
        "action": 0,
        "use_head_music": False,
        "use_tail_music": False,
        "audio_config": {
            "format": "mp3",
            "sample_rate": 24000,
            "speech_rate": 0
        },
        "speaker_info": {
            "random_order": True,
            "speakers": SPEAKERS
        },
        "input_info": {
            "return_audio_url": True,
            "input_text_max_length": 12000
        }
    }

    print(f"正在连接到火山引擎 TTS 服务...")
    print(f"文本长度: {len(text)} 字符")
    print(f"使用 APP_ID: {APP_ID}")

    audio_data = b""
    audio_url = None
    session_id = str(uuid.uuid4())

    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with websockets.connect(WS_URL, additional_headers=headers, ssl=ssl_context,
                                     close_timeout=180, ping_timeout=180) as ws:
            print("✅ WebSocket连接已建立\n")

            # 1. Start connection (event=1)
            await send_message(ws, MsgType.FullClientRequest, MsgTypeFlagBits.WithEvent,
                             EventType.StartConnection, payload=b'{}')

            # 2. Wait for ConnectionStarted (event=50)
            msg = await wait_for_event(ws, EventType.ConnectionStarted)
            print(f"✅ 连接已建立\n")

            # 3. Start session (event=100) with payload
            payload_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            await send_message(ws, MsgType.FullClientRequest, MsgTypeFlagBits.WithEvent,
                             EventType.StartSession, session_id, payload_bytes)

            # 4. Wait for SessionStarted (event=150)
            msg = await wait_for_event(ws, EventType.SessionStarted)
            print(f"✅ 会话已开始\n")

            # 5. Finish session (event=102)
            await send_message(ws, MsgType.FullClientRequest, MsgTypeFlagBits.WithEvent,
                             EventType.FinishSession, session_id, payload=b'{}')

            # 6. Receive messages
            round_audio = bytearray()
            current_round = None

            while True:
                msg = await receive_message(ws)

                # Podcast round start
                if msg['event'] == EventType.PodcastRoundStart:
                    if msg['payload']:
                        data = json.loads(msg['payload'].decode('utf-8'))
                        current_round = data.get("round_id")
                        speaker = data.get("speaker", "unknown")
                        text_content = data.get("text", "")
                        print(f"🎙️ 第 {current_round} 轮开始 - 说话人: {speaker}")
                        if text_content:
                            print(f"   内容: {text_content[:100]}...")

                # Podcast round response (audio data)
                elif msg['event'] == EventType.PodcastRoundResponse:
                    if msg['payload']:
                        audio_data += msg['payload']
                        round_audio.extend(msg['payload'])
                        print(f"   📦 收到音频数据: {len(msg['payload'])} 字节")

                # Podcast round end
                elif msg['event'] == EventType.PodcastRoundEnd:
                    if msg['payload']:
                        data = json.loads(msg['payload'].decode('utf-8'))
                        if data.get("is_error"):
                            print(f"❌ 轮次结束但有错误: {data}")
                        else:
                            print(f"✅ 第 {current_round} 轮结束\n")
                    round_audio.clear()

                # Podcast end
                elif msg['event'] == EventType.PodcastEnd:
                    if msg['payload']:
                        data = json.loads(msg['payload'].decode('utf-8'))
                        meta_info = data.get("meta_info", {})
                        audio_url = meta_info.get("audio_url")
                        if audio_url:
                            print(f"🔗 音频下载链接: {audio_url}\n")

                # Session finished
                elif msg['event'] == EventType.SessionFinished:
                    print(f"✅ 会话结束\n")
                    break

                # Usage response
                elif msg['event'] == EventType.UsageResponse:
                    if msg['payload']:
                        data = json.loads(msg['payload'].decode('utf-8'))
                        usage = data.get("usage", {})
                        print(f"📊 用量统计: {usage}\n")

            # 7. Finish connection (event=2)
            await send_message(ws, MsgType.FullClientRequest, MsgTypeFlagBits.WithEvent,
                             EventType.FinishConnection, payload=b'{}')

            # 8. Wait for ConnectionFinished (event=52)
            msg = await wait_for_event(ws, EventType.ConnectionFinished)
            print(f"✅ 连接已关闭\n")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"❌ 连接关闭: {e}")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 保存音频
    if audio_data:
        with open(output_file, "wb") as f:
            f.write(audio_data)
        print(f"✅ 音频已保存到: {output_file}")
        print(f"   文件大小: {len(audio_data) / 1024:.1f} KB\n")

    if audio_url:
        print(f"🔗 也可通过链接下载: {audio_url}\n")

    return True

async def main():
    parser = argparse.ArgumentParser(description="火山引擎 Podcast TTS")
    parser.add_argument("text", nargs="?", help="要转换的文本")
    parser.add_argument("-f", "--file", help="输入文件路径")
    parser.add_argument("-o", "--output", default="podcast.mp3", help="输出文件名")

    args = parser.parse_args()

    text = args.text

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif not text:
        print("请提供文本内容或输入文件")
        print("用法: python3 volc_podcast.py '要转换的文本' 或 python3 volc_podcast.py -f input.txt")
        sys.exit(1)

    if len(text) > 30000:
        text = text[:30000]
        print(f"⚠️  文本已截断至 30000 字符\n")

    await generate_podcast(text, args.output)

if __name__ == "__main__":
    asyncio.run(main())
