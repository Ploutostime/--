from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import os
from typing import List

MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
DEFAULT_COLLECTION = "documents_collection"
DIMENSION = int(os.getenv("EMBED_DIM", "1536"))  # 与 Embedding 模型输出维度一致

connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

def ensure_collection(name: str = DEFAULT_COLLECTION, dim: int = DIMENSION, shards: int = 2):
    if utility.has_collection(name):
        return Collection(name)
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=256),
    ]
    schema = CollectionSchema(fields, description="Documents embeddings")
    coll = Collection(name, schema=schema, shards_num=shards)
    # create index on vector field
    index_params = {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 1024}}
    coll.create_index(field_name="embedding", index_params=index_params)
    coll.load()
    return coll

def insert_vectors(collection: Collection, embeddings: List[List[float]], doc_ids: List[str]):
    # returns inserted primary keys
    entities = [
        embeddings,
        doc_ids,
    ]
    # order: fields other than pk (auto_id)
    res = collection.insert([list(range(len(embeddings))), embeddings, doc_ids])  # dummy pk column will be auto id; keep consistent shape
    # but safer: use only embedding and doc_id, since pk is auto
    # milvus returns primary keys
    return res.primary_keys

def search_vectors(collection: Collection, query_embedding: List[float], top_k: int = 4, params=None):
    collection.load()
    search_params = params or {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search([query_embedding], "embedding", search_params, top_k, output_fields=["doc_id"])
    # results is a list per query
    hits = []
    for hit in results[0]:
        hits.append({"milvus_id": str(hit.id), "score": float(hit.distance), "doc_id": hit.entity.get("doc_id")})
    return hits