from app.core.db import get_db_connection

def cache_exchange_rate(base_currency: str, target_currency: str, rate: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO exchange_rates (base_currency, target_currency, rate) VALUES (?, ?, ?)",
        (base_currency, target_currency, rate)
    )
    conn.commit()
    conn.close()
