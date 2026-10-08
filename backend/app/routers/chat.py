from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import ai_service

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)

@router.post("/", response_model=ChatResponse)
def chat_with_ai(request: ChatRequest):
    # Pass user message to our AI service
    ai_reply = ai_service.get_ai_response(request.message)
    return ChatResponse(reply=ai_reply)
