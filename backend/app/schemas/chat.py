from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    conversation_id: int = None # We will use this later to remember chat history

class ChatResponse(BaseModel):
    reply: str
