"""
Fashion Trends API Endpoints
Core API routes for trend discovery and analysis
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List, Dict, Any
from app.services.algolia_service import algolia_service
from app.models.trend import TrendResponse, TrendAnalysis, TrendSearchRequest
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def get_trends_and_search(
    query: Optional[str] = Query(None, description="Search query for trends"),
    category: Optional[str] = Query(None, description="Fashion category filter"),
    region: Optional[str] = Query(None, description="Geographic region filter"),
    limit: int = Query(20, ge=1, le=100, description="Number of trends to return"),
    page: int = Query(1, ge=1, description="Page number for pagination")
):
    """
    Get current fashion trends or search for specific trends.
    
    This single endpoint handles both browsing and searching.
    - To browse, leave the 'query' parameter empty.
    - To search, provide a term in the 'query' parameter.
    
    Filters for category and region can be applied in both modes.
    """
    try:
        page_zero_indexed = page - 1
        response = await algolia_service.search_trends(
            query=query or "",
            category=category,
            region=region,
            page=page_zero_indexed,
            per_page=limit
        )
        
        # Convert response to dict with correct field names (not aliases)
        response_dict = response.model_dump(by_alias=False)
        return response_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{trend_id}/analysis", response_model=TrendAnalysis)
async def analyze_trend(trend_id: str):
    """
    Get detailed analysis for a specific trend.
    """
    try:
        analysis = await algolia_service.get_trend_by_id(trend_id)
        if not analysis:
            raise HTTPException(status_code=404, detail=f"Trend with ID '{trend_id}' not found.")
        
        # In a real scenario, this would involve more complex analysis logic.
        # For now, we can structure the response from the retrieved trend data.
        return TrendAnalysis(
            trend_id=analysis.objectID,
            analysis={
                "popularity_score": analysis.trend_score * 100,
                "growth_prediction": f"Trend is growing at {analysis.growth_rate}%",
                "market_opportunity": "High" if analysis.trend_score > 0.8 else "Medium",
                "competitor_analysis": analysis.brand_adoptions,
                "recommendations": [
                    f"Target the {analysis.demographics.primary_age} age group.",
                    f"Focus marketing efforts in: {', '.join(analysis.regions)}."
                ]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories", response_model=List[str])
async def get_trend_categories():
    """
    Get a list of all available fashion trend categories from Algolia facets.
    """
    try:
        return await algolia_service.get_facet_values('category')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regions", response_model=List[str])
async def get_trend_regions():
    """
    Get a list of all available regions from Algolia facets.
    """
    try:
        return await algolia_service.get_facet_values('regions')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predict", response_model=Dict[str, Any])
async def predict_trends(
    category: Optional[str] = Query(None, description="Category to predict trends for"),
    timeframe: str = Query("next_month", description="Prediction timeframe"),
    confidence_threshold: float = Query(0.7, ge=0.0, le=1.0, description="Minimum confidence score")
):
    """
    Predict upcoming fashion trends
    
    🚀 THIS IS YOUR WINNING FEATURE! 🚀
    AI-powered trend prediction - not just current trends, but future ones!
    """
    try:
        # This is where you'd implement your ML prediction model
        # For the hackathon, you can start with mock data and build the real model later
        
        predicted_trends = {
            "predictions": [
                {
                    "trend_name": "Neo-Gothic Revival",
                    "category": category or "streetwear",
                    "confidence_score": 0.85,
                    "predicted_peak": "2025-03-15",
                    "growth_indicators": ["social_media_mentions", "runway_appearances"],
                    "regions": ["Europe", "North America"],
                    "description": "Dark romantic aesthetics with modern twists"
                },
                {
                    "trend_name": "Sustainable Luxury",
                    "category": category or "luxury",
                    "confidence_score": 0.92,
                    "predicted_peak": "2025-04-01",
                    "growth_indicators": ["eco_consciousness", "brand_adoptions"],
                    "regions": ["Global"],
                    "description": "High-end fashion with environmental responsibility"
                }
            ],
            "timeframe": timeframe,
            "confidence_threshold": confidence_threshold,
            "model_version": "1.0.0",
            "generated_at": "2025-01-24T23:15:00Z"
        }
        
        return {
            "success": True,
            "data": predicted_trends,
            "message": f"Generated {len(predicted_trends['predictions'])} trend predictions"
        }
        
    except Exception as e:
        logger.error(f"Error predicting trends: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to predict trends")

@router.get("/stats/combined", response_model=Dict[str, Any])
async def get_combined_stats():
    """
    Get combined statistics from both fashion_trends and fashion_news indices.
    """
    try:
        stats = await algolia_service.get_combined_stats()
        return {
            "success": True,
            "data": stats,
            "message": "Combined statistics retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting combined stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get combined statistics")