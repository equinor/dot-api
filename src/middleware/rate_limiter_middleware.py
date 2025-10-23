import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.config import config
from fastapi import status, HTTPException


class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore

        current_time = time.time()
        if current_time - config.LAST_REQUEST_TIME > config.RATE_LIMIT_WINDOW:
            config.REQUEST_COUNTER = 0
            config.LAST_REQUEST_TIME = current_time

        config.REQUEST_COUNTER += 1

        if config.REQUEST_COUNTER > config.MAX_REQUESTS_PER_WINDOW:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )
        response = await call_next(request)
        return response
