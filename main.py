import os
from typing import Optional, List
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from src.database.database import Database
from src.models.hardware_models import CPU
from src.routes import (
    cpu_router,
    ram_router,
    mainboard_router,
    storage_router,
    gpu_router,
    case_router,
    psu_router
)
from src.routes.order_routes import router as order_router
from src.routes.auth_routes import router as auth_router
from src.routes.admin_routes import router as admin_router
from src.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Computer Parts API",
    description="API for managing computer hardware components",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    # Configure OAuth2 for Swagger UI
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": "swagger-ui",
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify only allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database Connection
@app.on_event("startup")
async def startup_db_client():
    try:
        Database.get_instance()
        print("Database connection initialized")
    except Exception as e:
        print(f"Failed to initialize database connection: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    try:
        Database.close_connection()
        print("Database connection closed")
    except Exception as e:
        print(f"Error closing database connection: {e}")

# Custom OpenAPI to improve Swagger UI documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Computer Parts API",
        version="1.0.0",
        description="API for managing computer hardware components with JWT authentication",
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token in format: Bearer [token]"
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"Bearer Auth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Register routes with prefix
api_prefix = "/api/v1"
app.include_router(cpu_router, prefix=api_prefix)
app.include_router(ram_router, prefix=api_prefix)
app.include_router(mainboard_router, prefix=api_prefix)
app.include_router(storage_router, prefix=api_prefix)
app.include_router(gpu_router, prefix=api_prefix)
app.include_router(case_router, prefix=api_prefix)
app.include_router(psu_router, prefix=api_prefix)
app.include_router(order_router, prefix=api_prefix)
app.include_router(auth_router, prefix=api_prefix)
app.include_router(admin_router, prefix=api_prefix)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint providing API information and documentation links
    """
    return {
        "message": "Welcome to Computer Parts API",
        "version": "1.0.0",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "authentication_instructions": {
            "step1": "Register a new user at POST /api/v1/auth/register",
            "step2": "Login to get token at POST /api/v1/auth/login or /api/v1/auth/token (OAuth2)",
            "step3": "Use the token in Authorization header: Bearer <token>",
            "step4": "Access protected endpoints with the token"
        },
        "testing_auth": {
            "test_endpoint": "GET /api/v1/auth/me - Shows current user info",
            "swagger_ui": "In Swagger UI (/docs), click Authorize button and enter: Bearer <token>"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API and database status
    """
    try:
        db_status = "connected" if Database.is_connected() else "disconnected"
        return {
            "status": "healthy",
            "database": db_status,
            "api_version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    
    # Load configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "True").lower() == "true"
    workers = int(os.getenv("WORKERS", 1))
    
    # Configure logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_config=log_config
    )

