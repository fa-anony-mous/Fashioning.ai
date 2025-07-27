"""
AI Assistant API Endpoints
Provides intelligent fashion insights and recommendations using Gemini AI
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from app.services.gemini_service import gemini_service
from app.services.algolia_service import algolia_service
from app.services.advanced_ai_service import advanced_ai_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    type: str  # 'trend_analysis', 'style_advice', 'prediction', 'general'
    timestamp: str

class TrendAnalysisRequest(BaseModel):
    trend_id: str

class ComprehensiveAnalysisRequest(BaseModel):
    trend_id: str
    include_visualization: bool = False

class StyleRecommendationRequest(BaseModel):
    user_preferences: Dict[str, Any] = {}
    include_trends: bool = True
    limit: int = 5

@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """
    General AI chat endpoint for fashion-related questions
    """
    try:
        # Extract trend data from context if provided
        trend_data = None
        if request.context and request.context.get("trends") and len(request.context["trends"]) > 0:
            # Get the first trend from the context
            trend_data = request.context["trends"][0]
            # Update context to include trend_data for Gemini service
            request.context["trend_data"] = trend_data
        
        # Get current trends for context if not provided
        if not request.context or not request.context.get("trends"):
            trends_response = await algolia_service.search_trends("", page=0, per_page=10)
            trends_data = [trend.model_dump() for trend in trends_response.hits]
            
            if not request.context:
                request.context = {}
            request.context["trends"] = trends_data
        
        # Get AI response
        ai_response = await gemini_service.chat_response(request.message, request.context)
        
        # Determine response type based on content
        response_type = "general"
        if "trend" in request.message.lower() and "analyz" in request.message.lower():
            response_type = "trend_analysis"
        elif "recommend" in request.message.lower() or "style" in request.message.lower():
            response_type = "style_advice"
        elif "predict" in request.message.lower() or "future" in request.message.lower():
            response_type = "prediction"
        
        return {
            "success": True,
            "data": {
                "response": ai_response,
                "type": response_type,
                "message": request.message
            }
        }
        
    except Exception as e:
        logger.error(f"Error in AI chat: {e}")
        raise HTTPException(status_code=500, detail="Failed to process AI request")

@router.post("/analyze-trend")
async def analyze_specific_trend(request: TrendAnalysisRequest):
    """
    Get AI analysis for a specific trend
    """
    try:
        # Get trend data
        trend = await algolia_service.get_trend_by_id(request.trend_id)
        if not trend:
            raise HTTPException(status_code=404, detail="Trend not found")
        
        # Get AI analysis
        trend_data = trend.model_dump()
        analysis = await gemini_service.analyze_trend(trend_data)
        
        return {
            "success": True,
            "data": {
                "trend": trend_data,
                "analysis": analysis,
                "type": "trend_analysis"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing trend: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze trend")

@router.post("/comprehensive-analysis")
async def comprehensive_trend_analysis(request: ComprehensiveAnalysisRequest):
    """
    Get comprehensive AI analysis for a specific trend using multiple AI approaches
    """
    try:
        # Get trend data
        trend = await algolia_service.get_trend_by_id(request.trend_id)
        if not trend:
            raise HTTPException(status_code=404, detail="Trend not found")
        
        # Get comprehensive analysis
        trend_data = trend.model_dump()
        comprehensive_analysis = await advanced_ai_service.comprehensive_trend_analysis(trend_data)
        
        return {
            "success": True,
            "data": {
                "trend": trend_data,
                "comprehensive_analysis": comprehensive_analysis,
                "type": "comprehensive_analysis"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform comprehensive analysis")

@router.post("/style-recommendations")
async def get_style_recommendations(request: StyleRecommendationRequest):
    """
    Get personalized style recommendations
    """
    try:
        # Get current trends for context
        trends_data = []
        if request.include_trends:
            trends_response = await algolia_service.search_trends("", page=0, per_page=request.limit)
            trends_data = [trend.model_dump() for trend in trends_response.hits]
        
        # Get AI recommendations
        recommendations = await gemini_service.get_style_recommendations(
            request.user_preferences, 
            trends_data
        )
        
        return {
            "success": True,
            "data": {
                "recommendations": recommendations,
                "based_on_trends": trends_data[:3],  # Show which trends influenced the advice
                "type": "style_advice"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting style recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get style recommendations")

@router.get("/predict-trends")
async def predict_future_trends():
    """
    Get AI predictions for future fashion trends
    """
    try:
        # Get current trends for analysis
        trends_response = await algolia_service.search_trends("", page=0, per_page=20)
        trends_data = [trend.model_dump() for trend in trends_response.hits]
        
        # Get AI predictions
        predictions = await gemini_service.predict_future_trends(trends_data)
        
        return {
            "success": True,
            "data": {
                "predictions": predictions,
                "based_on": f"{len(trends_data)} current trends",
                "type": "prediction"
            }
        }
        
    except Exception as e:
        logger.error(f"Error predicting trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict trends")

@router.get("/ai-insights/{trend_id}")
async def get_trend_insights(trend_id: str):
    """
    Get AI-powered insights for a specific trend (quick access)
    """
    try:
        request = TrendAnalysisRequest(trend_id=trend_id)
        return await analyze_specific_trend(request)
        
    except Exception as e:
        logger.error(f"Error getting trend insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to get trend insights")

@router.get("/suggestions")
async def get_ai_suggestions():
    """
    Get suggested questions/prompts for the AI chat
    """
    suggestions = [
        "Analyze the top trending fashion item",
        "What style would suit me for summer?",
        "Predict what will be popular next season",
        "How can I incorporate sustainable fashion?",
        "What are the key color trends right now?",
        "Show me styling tips for professional wear",
        "What's driving the Y2K revival trend?",
        "How do I build a capsule wardrobe?"
    ]
    
    return {
        "success": True,
        "data": {
            "suggestions": suggestions,
            "categories": [
                "Trend Analysis",
                "Style Advice", 
                "Future Predictions",
                "Sustainability",
                "Color Trends",
                "Professional Styling"
            ]
        }
    } 