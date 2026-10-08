from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from app.database import Base

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String(255))
    file_url = Column(String(500))
    file_type = Column(String(50))
    status = Column(String(50))
    processing_error = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("knowledge_documents.id"))
    content = Column(String(5000))
    # Note: For pgvector, this would be Vector(1536), but using JSON/String as placeholder for local DB
    embedding = Column(JSON) 
    chunk_index = Column(Integer)
    metadata_info = Column(JSON, nullable=True)

class FAQ(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    question = Column(String(1000))
    answer = Column(String(2000))
    category = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AIConfiguration(Base):
    __tablename__ = "ai_configurations"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    assistant_name = Column(String(100))
    system_prompt = Column(String(5000))
    tone = Column(String(50))
    language = Column(String(100))
    welcome_message = Column(String(1000))
    fallback_message = Column(String(1000))
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=500)
    human_handoff_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AIInteraction(Base):
    __tablename__ = "ai_interactions"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    message_id = Column(Integer, ForeignKey("messages.id"))
    intent = Column(String(100))
    model = Column(String(100))
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    latency_ms = Column(Integer)
    tool_used = Column(String(255), nullable=True)
    resolved_by_ai = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
