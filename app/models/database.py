"""
Database models and session management for long-term memory.
Uses SQLite by default — no external database server needed.
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# SQLite database file
DATABASE_URL = "sqlite:///data/memory.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

class UserMemory(Base):
    """
    Stores long-term facts about users across conversations.
    Example: "User likes hiking", "User is a software developer"
    """
    __tablename__ = "user_memories"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)  # User's WhatsApp number
    key = Column(String)  # What we learned (e.g., "favorite_color")
    value = Column(Text)  # The fact (e.g., "blue")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserMemory {self.phone_number}: {self.key}={self.value}>"

class ConversationLog(Base):
    """
    Stores conversation history for context retrieval.
    Keeps last N messages per conversation.
    """
    __tablename__ = "conversation_logs"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    conversation_id = Column(String, index=True)  # Unique per chat thread
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    message_type = Column(String, default="text")  # text, image, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConversationLog {self.conversation_id}: {self.role}>"

class ContentViolation(Base):
    """
    Logs content violations for safety monitoring.
    """
    __tablename__ = "content_violations"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    violation_type = Column(String)  # medical, financial, legal, illegal, etc.
    original_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    handled = Column(Boolean, default=False)

def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")

def get_db():
    """Get a database session. Use as context manager or dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_memory(db, phone_number: str, key: str, value: str = None):
    """
    Get a memory entry or create it if it doesn't exist.
    Returns the memory object.
    """
    memory = db.query(UserMemory).filter(
        UserMemory.phone_number == phone_number,
        UserMemory.key == key
    ).first()

    if memory and value:
        memory.value = value
        memory.updated_at = datetime.utcnow()
        db.commit()
    elif not memory and value:
        memory = UserMemory(
            phone_number=phone_number,
            key=key,
            value=value
        )
        db.add(memory)
        db.commit()
        db.refresh(memory)

    return memory

def get_user_memories(db, phone_number: str):
    """Get all memories for a specific user."""
    return db.query(UserMemory).filter(
        UserMemory.phone_number == phone_number
    ).all()

def add_conversation_message(db, phone_number: str, conversation_id: str, 
                             role: str, content: str, message_type: str = "text"):
    """Add a message to the conversation log."""
    log = ConversationLog(
        phone_number=phone_number,
        conversation_id=conversation_id,
        role=role,
        content=content,
        message_type=message_type
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_conversation_history(db, conversation_id: str, limit: int = 20):
    """Get recent conversation history for context."""
    return db.query(ConversationLog).filter(
        ConversationLog.conversation_id == conversation_id
    ).order_by(ConversationLog.timestamp.desc()).limit(limit).all()

def cleanup_old_conversations(db, days: int = 7):
    """Remove conversation logs older than specified days."""
    cutoff = datetime.utcnow() - __import__("datetime").timedelta(days=days)
    db.query(ConversationLog).filter(ConversationLog.timestamp < cutoff).delete()
    db.commit()
