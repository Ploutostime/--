from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.api.routes import router as api_router
from src.app.api.websocket_routes import websocket_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(websocket_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Core Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)