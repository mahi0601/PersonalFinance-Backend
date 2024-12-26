from app.models.transactions import create_transaction

def add_transaction(user_id: int, amount: float, category: str, description: str):
    return create_transaction(user_id, amount, category, description)
