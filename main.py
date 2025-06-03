import asyncio
import datetime
import json
from fastapi import FastAPI, APIRouter
from valkey.asyncio import Valkey
from os import getenv
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import logging

logger = logging.getLogger(__name__)

app = FastAPI()
# cors

app.add_middleware(
    CORSMiddleware,
    allow_origins=getenv(
        "CORS_ORIGINS", "https://artale_front.virgil246.com,http://localhost:3000"
    ).split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

r = Valkey(host=getenv("REDIS_HOST", "localhost"), port=6379, db=0)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


api = APIRouter(prefix="/api", tags=["api"])


async def get_pubsub_message():
    """Get a Valkey pubsub instance."""
    pubsub = r.pubsub()
    await pubsub.subscribe(getenv("SSE_CHANNEL", "artale_maplestory"))
    while True:
        try:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=10
            )
            if message:
                logger.info(f"Received message: {message}")
                data = message["data"].decode("utf-8")
                # { username: 'Henry', channel: 'general', text: '週末有什麼活動嗎？' },
                json_data = json.loads(data)
                data = {
                    "username": f"{json_data.get('NickName', 'Unknown')}#{json_data.get('ProfileCode', '')}",
                    "channel": json_data.get("Channel", "general"),
                    "text": json_data.get("Text", ""),
                    "timestamp": datetime.datetime.now().isoformat(),
                }
                data = json.dumps(data, ensure_ascii=False)
                yield f"event: message\ndata: {data}\n\n"
            await asyncio.sleep(0.05)  # Simulate waiting for a new message
        except Exception as e:
            logger.error(f"Error getting message: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"


# This is a placeholder for the SSE endpoint
@api.get("/sse")
async def sse():
    return StreamingResponse(get_pubsub_message(), media_type="text/event-stream")


app.include_router(api)
