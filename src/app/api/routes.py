from fastapi import APIRouter, HTTPException
from typing import List
from ..core.conversation_service import ConversationService
from ..models.conversation import Conversation

router = APIRouter()
conversation_service = ConversationService()

@router.post("/conversations/", response_model=Conversation)
async def create_conversation(conversation: Conversation):
    return conversation_service.start_conversation(conversation)

@router.get("/conversations/", response_model=List[Conversation])
async def get_conversations():
    return conversation_service.get_all_conversations()

@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    conversation = conversation_service.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    success = conversation_service.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"detail": "Conversation deleted successfully"}