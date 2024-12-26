from fastapi import FastAPI, WebSocket



from app.core.db import init_db

# Initialize the database
init_db()

# # Create FastAPI app
# app = FastAPI()

# # Include routers
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
# app.include_router(exchange.router, prefix="/exchange", tags=["Exchange Rates"])
from fastapi import FastAPI
from app.api.auth import auth_router
from app.api.transactions import transaction_router
from app.api.exchange import exchange_router
from app.api.gpt import gpt_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(transaction_router, prefix="/transactions", tags=["Transactions"])
app.include_router(exchange_router, prefix="/exchange", tags=["Exchange Rates"])
app.include_router(gpt_router, prefix="/gpt", tags=["GPT Integration"])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected to WebSocket!")

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await ws_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_message(user_id, f"Message received: {data}")
    except:
        ws_manager.disconnect(user_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)