# backend/app/core/redis_manager.py
import redis.asyncio as redis
from app.core.config import settings

_redis = None

async def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis

async def publish_message(room_id: str, message: dict):
    r = await get_redis()
    await r.publish(f"room:{room_id}", json.dumps(message))