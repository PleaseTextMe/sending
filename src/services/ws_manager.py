import logging
from typing import Dict, List

from fastapi import WebSocket

from src.core.metrics import ACTIVE_WS_CONNECTIONS

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # login -> list of active connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, login: str):
        await websocket.accept()
        if login not in self.active_connections:
            self.active_connections[login] = []
            # Broadcast to everyone else that this user is online
            await self.broadcast({"type": "presence", "login": login, "status": "online"}, exclude_login=login)
            
        self.active_connections[login].append(websocket)
        ACTIVE_WS_CONNECTIONS.inc()
        logger.info(f"WebSocket connected for user: {login}")
        
        # Send current online users to the newly connected user
        online_users = list(self.active_connections.keys())
        await self.send_personal_message({"type": "sync_presence", "online_users": online_users}, login)

    async def disconnect(self, websocket: WebSocket, login: str):
        if login in self.active_connections:
            if websocket in self.active_connections[login]:
                self.active_connections[login].remove(websocket)
                ACTIVE_WS_CONNECTIONS.dec()
            if not self.active_connections[login]:
                del self.active_connections[login]
                # Broadcast offline status
                await self.broadcast({"type": "presence", "login": login, "status": "offline"})
        logger.info(f"WebSocket disconnected for user: {login}")

    async def broadcast(self, message: dict, exclude_login: str = None):
        for login, connections in self.active_connections.items():
            if login == exclude_login:
                continue
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to broadcast WS message to {login}: {e}")

    async def send_personal_message(self, message: dict, login: str):
        if login in self.active_connections:
            for connection in self.active_connections[login]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to send WS message to {login}: {e}")
