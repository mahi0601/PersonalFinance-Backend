from pydantic import BaseModel

class ExchangeRateResponse(BaseModel):
    base_currency: str
    target_currency: str
    rate: float
    timestamp: str
