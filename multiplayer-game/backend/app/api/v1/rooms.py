# backend/app/api/v1/rooms.py
from fastapi import APIRouter, WebSocket, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
import json
from app.core.config import settings
from app.core.redis_manager import redis, publish_message

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Временное хранилище комнат
connected_clients = {}

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, token: str = None):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
    except:
        user_id = f"guest_{hash(token or '') % 10000}"

    await websocket.accept()
    key = f"{room_id}:{user_id}"
    connected_clients[key] = websocket

    # Уведомим всех
    await publish_message(room_id, {
        "type": "player_joined",
        "payload": {"user_id": user_id}
    })

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            if msg["type"] == "action":
                # Отправляем всем через Redis
                await publish_message(room_id, {
                    "type": "player_action",
                    "payload": {**msg["payload"], "user_id": user_id}
                })
    except:
        pass
    finally:
        if key in connected_clients:
            del connected_clients[key]
        await publish_message(room_id, {
            "type": "player_left",
            "payload": {"user_id": user_id}
        })