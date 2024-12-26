from fastapi import APIRouter, HTTPException
from app.schemas.gpt import GPTRequest
from app.services.gpt_service import GPTService

gpt_router = APIRouter()

gpt_service = GPTService(api_key="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")

@gpt_router.post("/generate/")
def generate_gpt_response(request: GPTRequest):
    try:
        response = gpt_service.generate_response(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GPT Error: {str(e)}")
