"""
Pydantic models for fashion trends
Data validation and serialization for trend-related endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class Demographics(BaseModel):
    primary_age: str
    secondary_age: Optional[str] = None
    gender_split: Dict[str, int]

class Trend(BaseModel):
    objectID: str = Field(..., alias="object_id")
    name: str
    category: str
    description: str
    regions: List[str]
    brand: Optional[str] = None
    source: str
    source_url: Optional[str] = None
    image_url: Optional[str] = None
    trend_score: float
    growth_rate: float
    color_palette: List[str]
    demographics: Demographics
    sustainability_score: float
    predicted_peak: datetime
    social_mentions: int
    influencer_adoptions: int
    brand_adoptions: List[str]
    tags: List[str]
    images: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    type: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TrendResponse(BaseModel):
    hits: List[Trend]
    total: int
    page: int
    pages: int
    facets: Dict[str, Any]
    processing_time: float
    error: Optional[str] = None

class TrendAnalysis(BaseModel):
    trend_id: str
    analysis: Dict[str, Any]

class TrendSearchRequest(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    page: int = 1
    per_page: int = 20

class UserPreferences(BaseModel):
    preferred_categories: List[str] = []
    preferred_regions: List[str] = []
    style_preferences: List[str] = []
    price_range: Dict[str, float] = {"min": 0, "max": 1000}
    sustainability_focus: bool = False