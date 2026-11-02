import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, BigInteger, Integer, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    sequence_num: Mapped[int] = mapped_column(BigInteger, nullable=False)
    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    agent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True
    )
    session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_sessions.id", ondelete="SET NULL"), nullable=True
    )
    tool_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tool_arguments_sanitized: Mapped[dict] = mapped_column(JSONB, nullable=False)
    arguments_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    decision: Mapped[str] = mapped_column(String(50), nullable=False)
    matched_rule_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("policy_rules.id", ondelete="SET NULL"), nullable=True
    )
    evaluation_latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    prev_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    event_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("org_id", "sequence_num", name="uq_audit_org_seq"),
        Index("ix_audit_events_org_id", "org_id"),
        Index("ix_audit_events_sequence_num", "sequence_num"),
        Index("ix_audit_events_event_hash", "event_hash"),
    )

    if TYPE_CHECKING:
        organization: Mapped["Organization"] = relationship()
        agent: Mapped["Agent"] = relationship()
        session: Mapped["AgentSession"] = relationship()
        matched_rule: Mapped["PolicyRule"] = relationship()