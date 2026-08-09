import logging
from typing import Dict, List

from fastapi import WebSocket

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # login -> list of active connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, login: str):
        await websocket.accept()
        if login not in self.active_connections:
            self.active_connections[login] = []
        self.active_connections[login].append(websocket)
        logger.info(f"WebSocket connected for user: {login}")

    def disconnect(self, websocket: WebSocket, login: str):
        if login in self.active_connections:
            if websocket in self.active_connections[login]:
                self.active_connections[login].remove(websocket)
            if not self.active_connections[login]:
                del self.active_connections[login]
        logger.info(f"WebSocket disconnected for user: {login}")

    async def send_personal_message(self, message: dict, login: str):
        if login in self.active_connections:
            for connection in self.active_connections[login]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to send WS message to {login}: {e}")
