from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"WebSocket подключён: user_id={user_id}")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"WebSocket отключён: user_id={user_id}")
        else:
            print(f"Попытка отключить несуществующий WebSocket: user_id={user_id}")

    async def send_personal_message(self, message: dict, user_id: str):
        print(f"Отправка сообщения: {message} → user_id={user_id}")
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Ошибка отправки WebSocket user_id={user_id}: {e}")
        else:
            print(f"Нет активного WebSocket-соединения для user_id={user_id}")
