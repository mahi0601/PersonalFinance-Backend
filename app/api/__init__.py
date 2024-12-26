from fastapi import APIRouter
from app.api.auth import auth_router
from app.api.transactions import transaction_router
from app.api.exchange import exchange_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(transaction_router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(exchange_router, prefix="/exchange", tags=["Exchange Rates"])
