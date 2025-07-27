"""
Mock Data Service for Fashion Trends
Provides sample data when Algolia is not configured
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.models.trend import Trend, TrendResponse

# Sample fashion trends data
SAMPLE_TRENDS = [
    {
        "objectID": "trend_001",
        "name": "Sustainable Luxury Fashion",
        "category": "luxury",
        "description": "High-end fashion brands embracing eco-friendly materials and ethical production methods",
        "regions": ["Global"],
        "brand": "Stella McCartney",
        "source": "Vogue Runway",
        "source_url": "https://www.vogue.com/runway",
        "image_url": None,
        "trend_score": 0.92,
        "growth_rate": 22.8,
        "color_palette": ["#228B22", "#8B4513", "#F5F5DC"],
        "demographics": {
            "primary_age": "26-35",
            "secondary_age": "36-45",
            "gender_split": {"female": 70, "male": 30}
        },
        "sustainability_score": 0.95,
        "predicted_peak": (datetime.now() + timedelta(days=90)).isoformat(),
        "social_mentions": 28750,
        "influencer_adoptions": 156,
        "brand_adoptions": ["Stella McCartney", "Patagonia", "Eileen Fisher"],
        "tags": ["sustainable", "luxury", "eco-friendly"],
        "images": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "type": "emerging"
    },
    {
        "objectID": "trend_002",
        "name": "Y2K Revival Streetwear",
        "category": "streetwear",
        "description": "Early 2000s fashion making a comeback with metallic fabrics and futuristic accessories",
        "regions": ["North America", "Europe"],
        "brand": "Nike",
        "source": "Vogue Runway",
        "source_url": "https://www.vogue.com/runway",
        "image_url": None,
        "trend_score": 0.85,
        "growth_rate": 15.2,
        "color_palette": ["#C0C0C0", "#FF1493", "#00FFFF"],
        "demographics": {
            "primary_age": "18-25",
            "secondary_age": "26-35",
            "gender_split": {"female": 60, "male": 40}
        },
        "sustainability_score": 0.6,
        "predicted_peak": (datetime.now() + timedelta(days=60)).isoformat(),
        "social_mentions": 15420,
        "influencer_adoptions": 89,
        "brand_adoptions": ["Nike", "Adidas", "Urban Outfitters"],
        "tags": ["y2k", "streetwear", "retro"],
        "images": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "type": "peak"
    },
    {
        "objectID": "trend_003",
        "name": "Minimalist Athleisure",
        "category": "athleisure",
        "description": "Clean, simple athletic wear that seamlessly transitions from gym to street",
        "regions": ["North America", "Asia Pacific"],
        "brand": "Lululemon",
        "source": "Vogue Runway",
        "source_url": "https://www.vogue.com/runway",
        "image_url": None,
        "trend_score": 0.78,
        "growth_rate": 12.5,
        "color_palette": ["#FFFFFF", "#000000", "#808080"],
        "demographics": {
            "primary_age": "26-35",
            "secondary_age": "36-45",
            "gender_split": {"female": 65, "male": 35}
        },
        "sustainability_score": 0.75,
        "predicted_peak": (datetime.now() + timedelta(days=45)).isoformat(),
        "social_mentions": 12340,
        "influencer_adoptions": 67,
        "brand_adoptions": ["Lululemon", "Athleta", "Alo Yoga"],
        "tags": ["minimalist", "athleisure", "clean"],
        "images": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "type": "growing"
    }
]

SAMPLE_CATEGORIES = [
    "luxury", "streetwear", "sustainable", "casual", "formal", 
    "vintage", "minimalist", "maximalist", "athleisure", "avant-garde"
]

SAMPLE_REGIONS = [
    "Global", "North America", "Europe", "Asia Pacific", 
    "Australia", "Africa", "South America"
]

def get_mock_trends_response(
    query: str = "",
    category: str = None,
    region: str = None,
    page: int = 0,
    per_page: int = 20
) -> TrendResponse:
    """Get mock trends data with filtering and pagination"""
    
    # Filter trends based on parameters
    filtered_trends = SAMPLE_TRENDS.copy()
    
    if query:
        query_lower = query.lower()
        filtered_trends = [
            trend for trend in filtered_trends
            if (query_lower in trend["name"].lower() or
                query_lower in trend["description"].lower() or
                query_lower in trend["category"].lower())
        ]
    
    if category:
        filtered_trends = [
            trend for trend in filtered_trends
            if trend["category"].lower() == category.lower()
        ]
    
    if region:
        filtered_trends = [
            trend for trend in filtered_trends
            if region in trend["regions"]
        ]
    
    # Calculate pagination
    total = len(filtered_trends)
    start_idx = page * per_page
    end_idx = start_idx + per_page
    paginated_trends = filtered_trends[start_idx:end_idx]
    
    # Convert to Trend objects
    trends = [Trend(**trend) for trend in paginated_trends]
    
    return TrendResponse(
        hits=trends,
        total=total,
        page=page,
        pages=(total + per_page - 1) // per_page,
        facets={
            "category": {
                "luxury": 1,
                "streetwear": 1,
                "athleisure": 1,
                "casual": 1,
                "avant-garde": 1
            },
            "regions": {
                "Global": 2,
                "North America": 3,
                "Europe": 3,
                "Asia Pacific": 1
            }
        },
        processing_time=0.05
    )

def get_mock_categories() -> List[str]:
    """Get mock categories"""
    return SAMPLE_CATEGORIES

def get_mock_regions() -> List[str]:
    """Get mock regions"""
    return SAMPLE_REGIONS

def get_mock_trend_by_id(trend_id: str) -> Trend:
    """Get a specific trend by ID"""
    for trend_data in SAMPLE_TRENDS:
        if trend_data["objectID"] == trend_id:
            return Trend(**trend_data)
    return None 