from typing import Optional, List
from uuid import uuid4
from src.app.db import SessionLocal
from src.app.models import ConversationRecord, MessageRecord
from sqlalchemy import select


class ConversationService:
    """DB-backed conversation service"""
    def __init__(self):
        self.db = SessionLocal

    def start_conversation(self, user_id: Optional[str] = None) -> str:
        cid = str(uuid4())
        with self.db() as session:
            conv = ConversationRecord(id=cid, user_id=str(user_id) if user_id else None)
            session.add(conv)
            session.commit()
            session.refresh(conv)
            return conv.id

    def add_message(self, conversation_id: str, user_id: Optional[str], content: str, role: str = "user") -> dict:
        mid = str(uuid4())
        with self.db() as session:
            msg = MessageRecord(id=mid, conversation_id=str(conversation_id), user_id=str(user_id) if user_id else None, role=role, content=content)
            session.add(msg)
            session.commit()
            session.refresh(msg)
            return {"id": msg.id, "conversation_id": msg.conversation_id, "user_id": msg.user_id, "role": msg.role, "content": msg.content, "created_at": msg.created_at.isoformat()}

    def get_conversation(self, conversation_id: str) -> Optional[dict]:
        with self.db() as session:
            stmt = select(ConversationRecord).where(ConversationRecord.id == str(conversation_id))
            conv = session.execute(stmt).scalar_one_or_none()
            if not conv:
                return None
            stmt2 = select(MessageRecord).where(MessageRecord.conversation_id == str(conversation_id)).order_by(MessageRecord.created_at)
            rows = session.execute(stmt2).scalars().all()
            return {
                "id": conv.id,
                "user_id": conv.user_id,
                "messages": [{"id": r.id, "user_id": r.user_id, "role": r.role, "content": r.content, "created_at": r.created_at.isoformat()} for r in rows]
            }

    def list_conversations(self) -> List[dict]:
        with self.db() as session:
            stmt = select(ConversationRecord)
            convs = session.execute(stmt).scalars().all()
            out = []
            for c in convs:
                out.append({"id": c.id, "user_id": c.user_id, "created_at": c.created_at.isoformat()})
            return out