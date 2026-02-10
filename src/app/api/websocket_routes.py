from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from ..core.websocket_manager import WebSocketManager
from ..core.conversation_service import ConversationService

router = APIRouter()
manager = WebSocketManager()
conversation_service = ConversationService()

@router.websocket("/ws/conversation/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    await manager.connect(websocket, conversation_id)
    try:
        while True:
            data = await websocket.receive_text()
            response = conversation_service.handle_message(conversation_id, data)
            await manager.broadcast(conversation_id, response)
    except WebSocketDisconnect:
        manager.disconnect(websocket, conversation_id)