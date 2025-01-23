from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from libs.utils.logger import get_logger
from apps.weather_service.core.config import settings
from apps.ai_service.api.endpoints.ai import router as ai_router
import time
import uuid

logger = get_logger(__name__)
app = FastAPI(
    title="AI/ML Decision Service",
    description="A service that provides AI/ML-based decisions using weather data.",
    version="1.0.0",
)


@app.middleware("http")
async def add_request_id_and_log(request: Request, call_next):
    """
    Middleware to add a unique request ID to each request and log processing time.
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error(
            "Unhandled exception in middleware",
            extra={"request_id": request_id, "error": str(exc)},
        )
        raise exc

    process_time = time.time() - start_time

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.2f}"
    response.headers["X-Backend-Version"] = settings.PROJECT_NAME

    logger.info(
        "Request completed",
        extra={
            "request_id": request_id,
            "process_time": f"{process_time:.2f}s",
            "status_code": response.status_code,
            "path": request.url.path,
        },
    )
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler to catch unhandled exceptions and return a generic error response.
    """
    request_id = (
        request.state.request_id if hasattr(request.state, "request_id") else "unknown"
    )
    logger.error(
        "Unhandled exception", extra={"request_id": request_id, "error": str(exc)}
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred.", "request_id": request_id},
    )


app.include_router(ai_router, prefix="/api/v1", tags=["AI/ML"])
