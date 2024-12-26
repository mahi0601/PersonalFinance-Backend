from pydantic import BaseModel

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    category: str
    description: str

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    category: str
    description: str
    date: str
