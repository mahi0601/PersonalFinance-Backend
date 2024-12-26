from pydantic import BaseModel

class GPTRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class GPTResponse(BaseModel):
    response: str
