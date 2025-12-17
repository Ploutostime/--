from fastapi import APIRouter
from app.core.conversation_service import ConversationService

router = APIRouter()
conversation_service = ConversationService()

@router.post("/conversations/")
async def create_conversation(conversation_data: dict):
    return conversation_service.create_conversation(conversation_data)

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    return conversation_service.get_conversation(conversation_id)

@router.get("/conversations/")
async def list_conversations():
    return conversation_service.list_conversations()