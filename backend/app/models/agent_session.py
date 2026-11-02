import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Integer, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AgentSession(Base):
    __tablename__ = "agent_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False
    )
    external_session_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    total_tool_calls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    blocked_tool_calls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cumulative_cost_usd: Mapped[Decimal] = mapped_column(
        Numeric(10, 4), default=Decimal("0"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (
        Index("ix_agent_sessions_agent_id", "agent_id"),
        Index("ix_agent_sessions_external_session_id", "external_session_id"),
    )

    if TYPE_CHECKING:
        agent: Mapped["Agent"] = relationship(back_populates="sessions")