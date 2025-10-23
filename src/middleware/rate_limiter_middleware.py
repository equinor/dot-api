import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.config import config
from fastapi import status, HTTPException
from typing import Dict

rate_limit_mapper: Dict[str, int] = {}
last_request_time = time.time()


async def get_client_ip(request: Request) -> str:
    return request.client.host  # type: ignore


class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore
        global last_request_time, rate_limit_mapper
        client_ip = await get_client_ip(request)
        if not client_ip:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client IP missing",
            )

        current_time = time.time()
        if current_time - last_request_time > config.RATE_LIMIT_WINDOW:
            rate_limit_mapper = {}
            last_request_time = current_time

        rate_limit_mapper[client_ip] = rate_limit_mapper.get(client_ip, 0) + 1

        if rate_limit_mapper[client_ip] > config.MAX_REQUESTS_PER_WINDOW:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )

        response = await call_next(request)
        return response
