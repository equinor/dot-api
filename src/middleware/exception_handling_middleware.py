from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from src.logger import get_dot_api_logger
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.exceptions import RequestValidationError
from src.config import config

logger = get_dot_api_logger()


# Middleware for handling exceptions globally
class ExceptionFilterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore
        try:
            # Process request and response
            response = await call_next(request)
            return response
        except HTTPException as exc:
            # Log and return custom message for HTTP exceptions
            logger.error(f"HTTPException: {exc}")
            return JSONResponse(
                status_code=exc.status_code,
                content={"message": exc.detail},  # Use `detail` from HTTPException
            )
        except FileNotFoundError as exc:
            # Log the FileNotFoundError with details
            logger.error(f"FileNotFoundError: {exc}")
            return JSONResponse(status_code=404, content={"message": "File not found"})
        except RequestValidationError as exc:
            # Log and return validation errors
            logger.error(f"Validation error: {exc.errors()}")
            return JSONResponse(
                status_code=400, content={"message": "Validation error.", "errors": exc.errors()}
            )
        except Exception as exc:
            if config.APP_ENV == "local":
                logger.error(f"Unhandled exception: {str(exc)}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "message": f"Internal server error: {str(exc.args)}"
                    },  # Show detailed message
                )
            else:
                logger.error("Unhandled exception")
                return JSONResponse(
                    status_code=500, content={"message": "Internal server error"}  # Generic message
                )
