"""
User API Endpoints
User management and preferences for personalized fashion trends
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.models.trend import UserPreferences
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/profile")
async def get_user_profile():
    """
    Get user profile information
    
    For hackathon demo - shows personalization capabilities
    """
    # Mock user data for demo
    mock_profile = {
        "id": "user_123",
        "name": "Fashion Enthusiast",
        "email": "user@example.com",
        "preferences": {
            "preferred_categories": ["streetwear", "sustainable"],
            "preferred_regions": ["North America", "Europe"],
            "style_preferences": ["minimalist", "vintage"],
            "price_range": {"min": 50, "max": 300},
            "sustainability_focus": True
        },
        "trend_history": [
            {"trend_id": "trend_001", "interaction": "liked", "timestamp": "2025-01-20T10:00:00Z"},
            {"trend_id": "trend_002", "interaction": "saved", "timestamp": "2025-01-19T15:30:00Z"}
        ],
        "created_at": "2025-01-01T00:00:00Z"
    }
    
    return {
        "success": True,
        "data": mock_profile,
        "message": "User profile retrieved successfully"
    }

@router.put("/preferences")
async def update_user_preferences(preferences: UserPreferences):
    """
    Update user fashion preferences
    
    Key for personalization - shows AI learning from user behavior!
    """
    try:
        # In production, save to database
        # For demo, just return the updated preferences
        
        return {
            "success": True,
            "data": {
                "preferences": preferences.dict(),
                "updated_at": "2025-01-24T23:15:00Z"
            },
            "message": "Preferences updated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error updating preferences: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update preferences")

@router.get("/history")
async def get_user_history():
    """
    Get user's trend interaction history
    
    Shows engagement tracking for better personalization
    """
    mock_history = {
        "interactions": [
            {
                "trend_id": "trend_001",
                "trend_name": "Y2K Revival",
                "action": "liked",
                "timestamp": "2025-01-20T10:00:00Z"
            },
            {
                "trend_id": "trend_002", 
                "trend_name": "Sustainable Luxury",
                "action": "saved",
                "timestamp": "2025-01-19T15:30:00Z"
            },
            {
                "trend_id": "trend_003",
                "trend_name": "Neo-Gothic",
                "action": "shared",
                "timestamp": "2025-01-18T09:15:00Z"
            }
        ],
        "stats": {
            "total_interactions": 3,
            "most_liked_category": "streetwear",
            "engagement_score": 0.85
        }
    }
    
    return {
        "success": True,
        "data": mock_history,
        "message": "User history retrieved successfully"
    }