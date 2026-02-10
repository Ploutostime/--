import os
from typing import List, Optional
from langchain.embeddings import OpenAIEmbeddings
from milvus_client import ensure_collection
from src.app.db import SessionLocal
from src.app.models import DocumentRecord
from sqlalchemy import select

EMBED_DIM = int(os.getenv("EMBED_DIM", "1536"))


class RAGStoreMilvus:
    def __init__(self, collection_name: str = None, embedding_model=None):
        self.collection = ensure_collection(collection_name) if collection_name else ensure_collection()
        self.embedding_model = embedding_model or OpenAIEmbeddings()
        self.db = SessionLocal

    def add_documents(self, docs: List[str], metadatas: Optional[List[dict]] = None, sources: Optional[List[str]] = None):
        metadatas = metadatas or [{}] * len(docs)
        sources = sources or [None] * len(docs)
        embeddings = self.embedding_model.embed_documents(docs)
        with self.db() as session:
            session.expire_on_commit = False
            records = []
            for content, meta, src in zip(docs, metadatas, sources):
                rec = DocumentRecord(content=content, meta=meta, source=src)
                session.add(rec)
                records.append(rec)
            session.commit()
            doc_ids = [str(rec.id) for rec in records]
        from milvus_client import insert_vectors
        pk_list = insert_vectors(self.collection, embeddings, doc_ids)
        with self.db() as session:
            for rec_id, milvus_pk in zip(doc_ids, pk_list):
                stmt = select(DocumentRecord).where(DocumentRecord.id == int(rec_id))
                obj = session.execute(stmt).scalar_one()
                obj.milvus_id = str(milvus_pk)
                session.add(obj)
            session.commit()

    def retrieve(self, query: str, k: int = 4):
        q_emb = self.embedding_model.embed_query(query)
        from milvus_client import search_vectors
        hits = search_vectors(self.collection, q_emb, top_k=k)
        results = []
        with self.db() as session:
            for h in hits:
                doc_id = int(h.get("doc_id")) if h.get("doc_id") is not None else None
                if doc_id is None:
                    continue
                stmt = select(DocumentRecord).where(DocumentRecord.id == doc_id)
                row = session.execute(stmt).scalar_one_or_none()
                if not row:
                    continue
                results.append({
                    "text": row.content,
                    "score": h.get("score"),
                    "metadata": row.meta or {},
                    "source": row.source or "",
                    "milvus_id": row.milvus_id or "",
                })
        return results
