from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from app.database import create_db_and_tables, test_connection
from app.routers import auth_router, accounts_router, categories_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events - startup and shutdown"""
    # Startup
    print("🚀 Starting application...")
    
    # Test database connection
    if not test_connection():
        raise Exception("Failed to connect to database!")
    
    # Create tables
    create_db_and_tables()
    
    print("✅ Application started successfully!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down application...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    description="Personal Accounting Application API with double-entry bookkeeping"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(categories_router)


# Custom OpenAPI schema for Bearer authentication
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
    
#     openapi_schema = get_openapi(
#         title=settings.APP_NAME,
#         version=settings.APP_VERSION,
#         description="Accounting Application API with JWT authentication",
#         routes=app.routes,
#     )
    
#     openapi_schema["components"]["securitySchemes"] = {
#         "Bearer": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#             "description": "Enter your JWT access token"
#         }
#     }
    
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi


@app.get("/", tags=["Root"])
def root():
    """API root endpoint"""
    return {
        "message": f"{settings.APP_NAME} is running",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }