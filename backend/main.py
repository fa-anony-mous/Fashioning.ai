"""
Fashioning.ai - FastAPI Backend
Main application entry point for the fashion trend discovery platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import trends, users, news
from app.services.algolia_service import algolia_service

# Create FastAPI application
app = FastAPI(
    title="Fashioning.ai API",
    description="AI-powered fashion trend discovery and personalization platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_event():
    await algolia_service.close()

# Include API routers
app.include_router(trends.router, prefix="/api/v1/trends", tags=["trends"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(news.router, prefix="/api/v1/news", tags=["news"])

# Import and include AI router
from app.api.v1 import ai
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])

# Import and include data enrichment router
from app.api.v1 import data_enrichment
app.include_router(data_enrichment.router, prefix="/api/v1/enrichment", tags=["data-enrichment"])

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to Fashioning.ai API",
        "version": "1.0.0",
        "status": "healthy",
        "algolia_configured": bool(settings.ALGOLIA_APP_ID and settings.ALGOLIA_ADMIN_API_KEY)
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "fashioning-ai-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )