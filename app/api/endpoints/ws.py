from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
from redislite import Redis

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    redis = Redis("/tmp/celerydb.rdb")
    pubsub = redis.pubsub()
    pubsub.subscribe(f"user:{user_id}")
    print(f"WebSocket подключён: user_id={user_id}")

    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message["type"] == "message":
                data = json.loads(message["data"].decode())
                await websocket.send_json(data)
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print(f"WebSocket отключён: user_id={user_id}")
        pubsub.unsubscribe(f"user:{user_id}")
        pubsub.close()
