from fastapi import APIRouter, HTTPException
from src.app.core.conversation_service import ConversationService

router = APIRouter()
conversation_service = ConversationService()


@router.post("/conversations/")
async def create_conversation(payload: dict):
    user_id = payload.get("user_id") if isinstance(payload, dict) else None
    return conversation_service.start_conversation(user_id)


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    conv = conversation_service.get_conversation(conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


@router.get("/conversations/")
async def list_conversations():
    return conversation_service.list_conversations()
