"""
Fashion News API Endpoints
API routes for fashion news from the fashion_news index
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
from app.services.algolia_service import algolia_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/search", response_model=Dict[str, Any])
async def search_news(
    query: Optional[str] = Query(None, description="Search query for news"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Number of news items to return")
):
    """
    Search fashion news from the fashion_news index.
    """
    try:
        page_zero_indexed = page - 1
        response = await algolia_service.search_news(
            query=query or "",
            page=page_zero_indexed,
            per_page=limit
        )
        
        return {
            "success": True,
            "data": response,
            "message": f"Found {response['total']} news items"
        }
    except Exception as e:
        logger.error(f"Error searching news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest", response_model=Dict[str, Any])
async def get_latest_news(limit: int = Query(10, ge=1, le=50, description="Number of latest news items")):
    """
    Get the latest fashion news items.
    """
    try:
        response = await algolia_service.search_news(
            query="",
            page=0,
            per_page=limit
        )
        
        return {
            "success": True,
            "data": response,
            "message": f"Retrieved {len(response['hits'])} latest news items"
        }
    except Exception as e:
        logger.error(f"Error getting latest news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 