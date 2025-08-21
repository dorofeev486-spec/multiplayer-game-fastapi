from fastapi import WebSocket
from typing import Dict, List
import asyncio
from app.core.redis_manager import publish_message

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, room_id: str, message: dict):
        if room_id in self.active_connections:
            for ws in self.active_connections[room_id]:
                await ws.send_json(message)
        # Также публикуем в Redis для других инстансов
        await publish_message(f"room:{room_id}", message)

manager = ConnectionManager()
