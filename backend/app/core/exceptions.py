from typing import Any
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str | None = None


def create_problem_detail(
    status_code: int,
    title: str,
    detail: str,
    instance: str | None = None,
    error_type: str | None = None,
) -> ProblemDetail:
    return ProblemDetail(
        type=error_type or f"https://httpstatuses.com/{status_code}",
        title=title,
        status=status_code,
        detail=detail,
        instance=instance,
    )


class PayloadTooLargeMiddleware:
    """ASGI middleware that rejects request bodies larger than MAX_PAYLOAD_SIZE_BYTES."""

    def __init__(self, app: Any, max_bytes: int) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        if scope["type"] == "http":
            content_length = scope.get("headers", [])
            content_length_value = None
            for key, value in content_length:
                if key == b"content-length":
                    content_length_value = int(value.decode())
                    break

            if content_length_value is not None and content_length_value > self.max_bytes:
                response = JSONResponse(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content=create_problem_detail(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        title="Payload Too Large",
                        detail=f"Request body exceeds maximum allowed size of {self.max_bytes} bytes",
                    ).model_dump(),
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)