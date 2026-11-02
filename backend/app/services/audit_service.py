from datetime import timezone
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.models.audit_event import AuditEvent
from app.core.crypto_ledger import compute_event_hash


async def append_event(
    db: AsyncSession,
    org_id: UUID,
    tool_name: str,
    tool_arguments_sanitized: dict,
    arguments_sha256: str,
    decision: str,
    created_at,
    agent_id: UUID | None = None,
    session_id: UUID | None = None,
    matched_rule_id: UUID | None = None,
    evaluation_latency_ms: int = 0,
) -> AuditEvent:
    # Acquire transaction-scoped advisory lock for the org
    await db.execute(
        text("SELECT pg_advisory_xact_lock(hashtext(:org_id))"),
        {"org_id": str(org_id)},
    )

    # Query the latest audit event for this org
    result = await db.execute(
        select(AuditEvent)
        .where(AuditEvent.org_id == org_id)
        .order_by(desc(AuditEvent.sequence_num))
        .limit(1)
    )
    last = result.scalar_one_or_none()

    sequence_num = (last.sequence_num + 1) if last else 1
    prev_hash = last.event_hash if last else ("0" * 64)

    # Normalize created_at to UTC ISO-8601
    if hasattr(created_at, "astimezone"):
        created_at_iso = created_at.astimezone(timezone.utc).isoformat()
    else:
        created_at_iso = str(created_at)

    # Compute event hash
    event_hash = compute_event_hash(
        prev_hash=prev_hash,
        sequence_num=sequence_num,
        org_id=str(org_id),
        agent_id=str(agent_id) if agent_id else "",
        tool_name=tool_name,
        arguments_sha256=arguments_sha256,
        decision=decision,
        created_at_iso=created_at_iso,
    )

    event = AuditEvent(
        org_id=org_id,
        agent_id=agent_id,
        session_id=session_id,
        sequence_num=sequence_num,
        tool_name=tool_name,
        tool_arguments_sanitized=tool_arguments_sanitized,
        arguments_sha256=arguments_sha256,
        decision=decision,
        matched_rule_id=matched_rule_id,
        evaluation_latency_ms=evaluation_latency_ms,
        prev_hash=prev_hash,
        event_hash=event_hash,
        created_at=created_at,
    )

    db.add(event)
    await db.flush()
    return event


async def verify_org_chain(db: AsyncSession, org_id: UUID) -> dict:
    result = await db.execute(
        select(AuditEvent)
        .where(AuditEvent.org_id == org_id)
        .order_by(AuditEvent.sequence_num.asc())
    )
    events = result.scalars().all()

    total_checked = len(events)
    broken_at_sequence: int | None = None
    latest_hash = ""

    if total_checked == 0:
        return {"is_valid": True, "total_checked": 0, "broken_at_sequence": None, "latest_hash": ""}

    prev_event_hash = "0" * 64
    expected_sequence = 1

    for event in events:
        latest_hash = event.event_hash

        # Check sequence_num continuity
        if event.sequence_num != expected_sequence:
            broken_at_sequence = event.sequence_num
            return {
                "is_valid": False,
                "total_checked": total_checked,
                "broken_at_sequence": broken_at_sequence,
                "latest_hash": latest_hash,
            }

        # Check prev_hash linkage
        if event.prev_hash != prev_event_hash:
            broken_at_sequence = event.sequence_num
            return {
                "is_valid": False,
                "total_checked": total_checked,
                "broken_at_sequence": broken_at_sequence,
                "latest_hash": latest_hash,
            }

        # Recompute and verify event_hash
        from app.core.crypto_ledger import compute_event_hash
        from datetime import timezone

        created_at_iso = (
            event.created_at.astimezone(timezone.utc).isoformat()
            if hasattr(event.created_at, "astimezone")
            else str(event.created_at)
        )

        recomputed_hash = compute_event_hash(
            prev_hash=event.prev_hash,
            sequence_num=event.sequence_num,
            org_id=str(event.org_id),
            agent_id=str(event.agent_id) if event.agent_id else "",
            tool_name=event.tool_name,
            arguments_sha256=event.arguments_sha256,
            decision=event.decision,
            created_at_iso=created_at_iso,
        )

        if recomputed_hash != event.event_hash:
            broken_at_sequence = event.sequence_num
            return {
                "is_valid": False,
                "total_checked": total_checked,
                "broken_at_sequence": broken_at_sequence,
                "latest_hash": latest_hash,
            }

        prev_event_hash = event.event_hash
        expected_sequence += 1

    return {
        "is_valid": True,
        "total_checked": total_checked,
        "broken_at_sequence": None,
        "latest_hash": latest_hash,
    }