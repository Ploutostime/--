import os
import json
import traceback
from dotenv import load_dotenv

load_dotenv()

results = {"db": None, "milvus": None}

print("Starting smoke test...")

try:
    from src.app.db import engine
    with engine.connect() as conn:
        r = conn.execute("SELECT 1")
        results["db"] = {"ok": True, "detail": str(list(r))}
        print("DB: ok")
except Exception as e:
    results["db"] = {"ok": False, "error": str(e), "trace": traceback.format_exc()}
    print("DB: error", e)

try:
    from pymilvus import connections, utility
    host = os.getenv("MILVUS_HOST", "localhost")
    port = os.getenv("MILVUS_PORT", "19530")
    connections.connect(host=host, port=port)
    # check connection by listing collections (may raise)
    cols = utility.list_collections()
    results["milvus"] = {"ok": True, "collections": cols}
    print("Milvus: ok, collections:", cols)
except Exception as e:
    results["milvus"] = {"ok": False, "error": str(e), "trace": traceback.format_exc()}
    print("Milvus: error", e)

print("\nSmoke test results summary:\n")
print(json.dumps(results, indent=2, ensure_ascii=False))
