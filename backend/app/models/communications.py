from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from app.database import Base
import enum

class ChannelEnum(enum.Enum):
    WEBSITE = "WEBSITE"
    WHATSAPP = "WHATSAPP"

class ConversationStatusEnum(enum.Enum):
    AI_ACTIVE = "AI_ACTIVE"
    HUMAN_ACTIVE = "HUMAN_ACTIVE"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class SenderTypeEnum(enum.Enum):
    CUSTOMER = "CUSTOMER"
    AI = "AI"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    channel = Column(Enum(ChannelEnum))
    status = Column(Enum(ConversationStatusEnum))
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    last_message_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender_type = Column(Enum(SenderTypeEnum))
    content = Column(String(5000))
    message_type = Column(String(50))
    metadata_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    subject = Column(String(255))
    description = Column(String(2000))
    priority = Column(String(50))
    status = Column(String(50))
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AgentAssignment(Base):
    __tablename__ = "agent_assignments"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    agent_id = Column(Integer, ForeignKey("users.id"))
    assigned_at = Column(DateTime, default=func.now())
    unassigned_at = Column(DateTime, nullable=True)
    status = Column(String(50))
