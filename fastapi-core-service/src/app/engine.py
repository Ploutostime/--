import os
import json
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

from rag_store_milvus import RAGStoreMilvus as RAGStore

class PersonaManager:
    def __init__(self, path: str = "personas.json"):
        self.path = path
        self.personas = self._load()

    def _load(self) -> Dict[str, Dict]:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        default = {
            "agri_expert": {"name": "农业专家", "instruction": "你是一个专业的农业顾问，回答应简洁、有行动建议、引用可靠来源。"},
            "friendly_bot": {"name": "亲切助手", "instruction": "你是一个语气亲切的助手，回答通俗易懂、鼓励用户。"}
        }
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)
        return default

    def get(self, persona_id: str) -> Dict:
        return self.personas.get(persona_id, {"name": "default", "instruction": ""})

    def add(self, persona_id: str, name: str, instruction: str):
        self.personas[persona_id] = {"name": name, "instruction": instruction}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.personas, f, ensure_ascii=False, indent=2)

class AgentOrchestrator:
    def __init__(self, llm=None, rag_store: Optional[RAGStore] = None, persona_manager: Optional[PersonaManager] = None):
        self.llm = llm or OpenAI(temperature=0.2)
        self.rag = rag_store or RAGStore()
        self.personas = persona_manager or PersonaManager()
        self.template = PromptTemplate(
            input_variables=["persona_instruction", "context", "user_input"],
            template=(
                "Persona 指令：{persona_instruction}\n\n"
                "检索到的参考资料（只使用相关段落并在回答末尾列出来源）:\n{context}\n\n"
                "用户问题：{user_input}\n\n"
                "请给出简洁的回答，列出必要的步骤或建议，若不确定请说明并提供可验证的参考。"
            ),
        )

    def _build_context_str(self, retrieved: List[dict]) -> str:
        if not retrieved:
            return "（未检索到相关资料）"
        parts = []
        for i, r in enumerate(retrieved, 1):
            src = r.get("source") or r.get("metadata", {}).get("source") or f"doc#{i}"
            parts.append(f"[{src}] (score:{r.get('score'):.3f}):\n{r.get('text')}")
        return "\n\n".join(parts)

    def run(self, user_input: str, persona_id: str = "agri_expert", k: int = 4) -> Tuple[str, List[dict]]:
        persona = self.personas.get(persona_id)
        retrieved = self.rag.retrieve(user_input, k=k)
        context_str = self._build_context_str(retrieved)
        prompt = self.template.format(persona_instruction=persona.get("instruction", ""), context=context_str, user_input=user_input)
        answer = self.llm(prompt)
        return answer, retrieved
