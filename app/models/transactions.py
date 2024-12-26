from app.core.db import get_db_connection

def create_transaction(user_id: int, amount: float, category: str, description: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO transactions (user_id, amount, category, description) 
           VALUES (?, ?, ?, ?)""",
        (user_id, amount, category, description)
    )
    conn.commit()
    conn.close()
