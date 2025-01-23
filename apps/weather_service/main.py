from fastapi import FastAPI, Request, HTTPException
from libs.utils.logger import get_logger
from apps.weather_service.core.config import settings
from libs.utils.api_client import fetch_weather
from libs.utils.weather_logic import should_go_out
from apps.weather_service.api.endpoints.weather import router as weather_router
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError
from apps.weather_service.db.session import SessionLocal
import time
import uuid

logger = get_logger(__name__)
app = FastAPI()


# Middleware for adding request ID and response time logging
@app.middleware("http")
async def add_request_id_and_log(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error(
            "Unhandled error during request processing",
            extra={"request_id": request_id, "error": str(exc)},
        )
        raise
    finally:
        process_time = time.time() - start_time
        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "process_time": process_time,
                "path": request.url.path,
            },
        )

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Backend-Version"] = settings.PROJECT_NAME
    return response


# Middleware for database session lifecycle management
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    try:
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Global exception handler for unexpected errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = request.state.request_id
    logger.error(
        "Unhandled Exception",
        extra={"request_id": request_id, "error": str(exc)},
    )
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred.", "request_id": request_id},
    )


# Exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = request.state.request_id
    logger.warning(
        "HTTP Exception",
        extra={
            "request_id": request_id,
            "status_code": exc.status_code,
            "detail": exc.detail,
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "request_id": request_id},
    )


# Exception handler for database errors
@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    request_id = request.state.request_id
    logger.error(
        "Database Error",
        extra={"request_id": request_id, "error": str(exc)},
    )
    return JSONResponse(
        status_code=500,
        content={"error": "A database error occurred.", "request_id": request_id},
    )


# Ensure critical environment variables are loaded
if not settings.OPENWEATHER_API_KEY:
    logger.warning("Critical environment variable 'OPENWEATHER_API_KEY' is missing.")


# Define the weather decision endpoint
@app.get("/decision")
def weather_decision(city: str):
    """
    Get a decision on whether it's suitable to go out based on weather conditions.

    Args:
        city (str): Name of the city.

    Returns:
        dict: Decision and reasoning.
    """
    api_key = settings.OPENWEATHER_API_KEY
    if not api_key:
        raise HTTPException(status_code=500, detail="API key is not configured")

    try:
        weather_data = fetch_weather(api_key, city)
        return should_go_out(weather_data, city)
    except Exception as exc:
        logger.error(
            "Error fetching or processing weather data", extra={"error": str(exc)}
        )
        raise HTTPException(status_code=500, detail="Failed to process weather data")


# Include other API routes
app.include_router(weather_router, prefix="/api/v1", tags=["Weather"])
