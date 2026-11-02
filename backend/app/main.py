from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, async_session_maker
from app.redis_client import ping_redis

app = FastAPI(title="TrustLayer AI Backend", version="0.1.0")


@app.get("/api/v1/health")
async def health():
    db_status = "unknown"
    redis_status = "unknown"

    # Check DB
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    # Check Redis
    try:
        if await ping_redis():
            redis_status = "healthy"
        else:
            redis_status = "unhealthy"
    except Exception:
        redis_status = "unhealthy"

    overall = "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded"

    return {
        "status": overall,
        "database": db_status,
        "redis": redis_status,
    }