from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Index, func
from app.core.database import Base


class ChatMessage(Base):
    """Persistent chat history for the Smart Assistant.

    Each row stores one turn (user or assistant) within a session.
    Nullable user_id allows guest sessions; linking to users.id when authenticated.
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), nullable=False, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    role = Column(String(20), nullable=False)  # user | assistant | function
    content = Column(Text, nullable=False)
    function_call = Column(JSON, nullable=True)   # {"name": "search_locations", "args": {...}}
    language = Column(String(5), nullable=True)   # ar | en | de — for analytics

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Composite index for fast "last N messages in session" queries
    __table_args__ = (
        Index("ix_chat_messages_session_created", "session_id", "created_at"),
    )
