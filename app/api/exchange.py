import requests
from fastapi import APIRouter, HTTPException
from app.core.db import get_db_connection

exchange_router = APIRouter()

API_URL = "https://api.exchangerate-api.com/v4/latest/"

@exchange_router.get("/{base_currency}/")
def get_exchange_rate(base_currency: str, target_currency: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT rate, timestamp FROM exchange_rates WHERE base_currency = ? AND target_currency = ?",
        (base_currency, target_currency)
    )
    cached_rate = cursor.fetchone()
    if cached_rate:
        return {"rate": cached_rate["rate"], "timestamp": cached_rate["timestamp"]}

    response = requests.get(f"{API_URL}{base_currency}")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch exchange rate")

    data = response.json()
    rate = data["rates"].get(target_currency)
    if not rate:
        raise HTTPException(status_code=400, detail="Invalid target currency")

    cursor.execute(
        "INSERT INTO exchange_rates (base_currency, target_currency, rate) VALUES (?, ?, ?)",
        (base_currency, target_currency, rate)
    )
    conn.commit()
    conn.close()
    return {"rate": rate, "timestamp": data["time_last_updated"]}
