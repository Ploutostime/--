from fastapi import APIRouter, HTTPException
from typing import Optional
from src.app.core.conversation_service import ConversationService

router = APIRouter()
conversation_service = ConversationService()


@router.post("/conversations/")
async def create_conversation(payload: dict):
    user_id = payload.get("user_id") if isinstance(payload, dict) else None
    return conversation_service.start_conversation(user_id)


@router.post("/conversations/{conversation_id}/messages")
async def post_message(conversation_id: str, payload: dict):
    user_id = payload.get("user_id") if isinstance(payload, dict) else None
    content = payload.get("content") if isinstance(payload, dict) else None
    from fastapi import APIRouter, HTTPException
    from typing import Optional
    from src.app.core.conversation_service import ConversationService

    router = APIRouter()
    conversation_service = ConversationService()


    @router.post("/conversations/")
    async def create_conversation(payload: dict):
        user_id = payload.get("user_id") if isinstance(payload, dict) else None
        return conversation_service.start_conversation(user_id)


    @router.post("/conversations/{conversation_id}/messages")
    async def post_message(conversation_id: str, payload: dict):
        user_id = payload.get("user_id") if isinstance(payload, dict) else None
        content = payload.get("content") if isinstance(payload, dict) else None
        if not content:
            raise HTTPException(status_code=400, detail="Missing content")
        return conversation_service.add_message(conversation_id, user_id, content)


    @router.get("/conversations/{conversation_id}")
    async def get_conversation(conversation_id: str):
        conv = conversation_service.get_conversation(conversation_id)
        if conv is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conv


    @router.get("/conversations/")
    async def list_conversations():
        return conversation_service.list_conversations()