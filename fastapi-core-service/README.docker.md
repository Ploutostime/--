# Docker Compose (Postgres + Milvus + App)

Quick start (requires Docker & Docker Compose):

1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` if you need LLM access:

   ```powershell
   copy .\src\app\.env.example .env
   # edit .env to set OPENAI_API_KEY if needed
   ```

2. Start services:

   ```powershell
   cd "c:\Users\win\Desktop\新建文件夹\fastapi-core-service\fastapi-core-service"
   docker compose up --build -d
   ```

3. Verify:
   - FastAPI at http://localhost:8000/
   - Milvus gRPC at localhost:19530, HTTP at http://localhost:19121
   - Postgres at localhost:5432 (user: postgres, password: postgres, db: agri_db)

4. Stop services:

   ```powershell
   docker compose down -v
   ```
