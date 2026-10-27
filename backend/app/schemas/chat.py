from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    history: Optional[List[Dict[str, Any]]] = None

class ChatResponse(BaseModel):
    reply: str
