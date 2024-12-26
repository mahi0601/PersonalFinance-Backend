import requests
from app.models.exchange_rates import cache_exchange_rate

API_URL = "https://api.exchangerate-api.com/v4/latest/"

def fetch_exchange_rate(base_currency: str, target_currency: str):
    response = requests.get(f"{API_URL}{base_currency}")
    if response.status_code != 200:
        raise ValueError("Failed to fetch exchange rate")
    data = response.json()
    rate = data["rates"].get(target_currency)
    if not rate:
        raise ValueError("Invalid target currency")
    cache_exchange_rate(base_currency, target_currency, rate)
    return rate
