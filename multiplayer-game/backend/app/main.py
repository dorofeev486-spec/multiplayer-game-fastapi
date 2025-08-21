# backend/app/main.py
from fastapi import FastAPI
from app.api.v1 import auth, rooms, health

app = FastAPI(title="Multiplayer Game")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["rooms"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Game server is running!"}