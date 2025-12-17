from pathlib import Path
import json
import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from dotenv import load_dotenv

from core.websocket_manager import WebSocketManager
from core.conversation_service import ConversationService
from engine import AgentOrchestrator, PersonaManager
from rag_store_milvus import RAGStoreMilvus

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="以农为本 - 智能体网站")

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
else:
    print("Warning: static dir not found:", STATIC_DIR)

@app.get("/", include_in_schema=False)
async def root():
    f = STATIC_DIR / "初始页面.html"
    return FileResponse(str(f)) if f.exists() else RedirectResponse(url="/static/初始页面.html")

@app.get("/login", include_in_schema=False)
async def login_page():
    f = STATIC_DIR / "登录.html"
    return FileResponse(str(f)) if f.exists() else RedirectResponse(url="/static/登录.html")

@app.get("/register", include_in_schema=False)
async def register_page():
    f = STATIC_DIR / "注册.html"
    return FileResponse(str(f)) if f.exists() else RedirectResponse(url="/static/注册.html")

ws_manager = WebSocketManager()
conv_service = ConversationService()
_persona_manager = PersonaManager(path=str(Path.cwd() / "personas.json"))
_rag = RAGStoreMilvus()
_agent = AgentOrchestrator(rag_store=_rag, persona_manager=_persona_manager)

@app.post("/api/ask")
async def api_ask(request: Request):
    body = await request.json()
    question = body.get("question") or body.get("q") or ""
    persona = body.get("persona", "agri_expert")
    user_id = body.get("user_id")
    conversation_id = body.get("conversation_id")

    if not question:
        return JSONResponse({"error": "empty question"}, status_code=400)

    if not conversation_id:
        conv = conv_service.start_conversation(uuid.UUID(user_id) if user_id else None)
        conversation_id = str(conv.id)
    else:
        conv = conv_service.get_conversation(uuid.UUID(conversation_id))

    answer, retrieved = _agent.run(question, persona_id=persona)

    conv_service.add_message(uuid.UUID(conversation_id), uuid.UUID(user_id) if user_id else None, question, role="user")
    conv_service.add_message(uuid.UUID(conversation_id), uuid.UUID(user_id) if user_id else None, answer, role="assistant")

    return {"conversation_id": conversation_id, "answer": answer, "references": retrieved}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await ws_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                packet = json.loads(data)
            except Exception:
                packet = {"text": data}
            text = packet.get("text") or packet.get("q") or ""
            persona = packet.get("persona", "agri_expert")
            conversation_id = packet.get("conversation_id")

            if not conversation_id:
                conv = conv_service.start_conversation()
                conversation_id = str(conv.id)

            conv_service.add_message(uuid.UUID(conversation_id), None, text, role="user")
            answer, retrieved = _agent.run(text, persona_id=persona)
            conv_service.add_message(uuid.UUID(conversation_id), None, answer, role="assistant")

            resp = {"conversation_id": conversation_id, "answer": answer, "references": retrieved}
            await ws_manager.send_message(user_id, json.dumps(resp))
    except WebSocketDisconnect:
        await ws_manager.disconnect(user_id)
