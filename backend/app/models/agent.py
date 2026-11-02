import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Boolean, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    api_key_prefix: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    api_key_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    killswitch_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    max_calls_per_session: Mapped[int] = mapped_column(default=50, nullable=False)
    max_cost_per_session_usd: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=Decimal("10.0"), nullable=False)
    default_fail_mode: Mapped[str] = mapped_column(String(20), default="FAIL_CLOSED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_agents_org_id", "org_id"),
    )

    if TYPE_CHECKING:
        organization: Mapped["Organization"] = relationship(back_populates="agents")
        sessions: Mapped[list["AgentSession"]] = relationship(back_populates="agent")