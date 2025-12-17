from dotenv import load_dotenv
load_dotenv()

from engine import AgentOrchestrator, PersonaManager
from rag_store_milvus import RAGStoreMilvus

def main():
    pm = PersonaManager(path="personas.json")
    rag = RAGStoreMilvus()
    agent = AgentOrchestrator(rag_store=rag, persona_manager=pm)

    # 示例文档（首次运行填充）
    docs = [
        "小麦栽培最佳温度在15-25摄氏度，注意排水与施氮管理。来源: 农业科技手册。",
        "玉米需肥量较高，生育中期补氮可提高产量。来源: 作物营养学资料。"
    ]
    rag.add_documents(docs, metadatas=[{"source":"手册A"},{"source":"手册B"}], sources=["手册A","手册B"])
    print("已填充示例文档到 Milvus 与数据库。")

    user_q = "现在小麦长出三叶，如何施肥？"
    answer, retrieved = agent.run(user_q, persona_id="agri_expert")
    print("回答：\n", answer)
    print("\n检索到的参考：")
    for r in retrieved:
        print("-", r.get("source"), "score:", r.get("score"))

if __name__ == "__main__":
    main()
