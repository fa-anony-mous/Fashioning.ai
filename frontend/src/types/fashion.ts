export interface FashionTrend {
  objectID: string;
  name: string;
  category: string;
  description: string;
  regions: string[];
  brand: string;
  source: string;
  source_url?: string;
  image_url?: string;
  trend_score: number;
  growth_rate: number;
  color_palette: string[];
  demographics: {
    primary_age: string;
    secondary_age?: string;
    gender_split: {
      female: number;
      male: number;
    };
  };
  sustainability_score: number;
  predicted_peak: string;
  social_mentions: number;
  influencer_adoptions: number;
  brand_adoptions: string[];
  tags: string[];
  images?: string[];
  created_at: string;
  updated_at: string;
  type?: string;
}

export interface TrendsResponse {
  success: boolean;
  data: {
    hits: FashionTrend[];
    total: number;
    page: number;
    pages: number;
    facets: Record<string, any>;
    processing_time: number;
  };
  message: string;
}

export interface SearchParams {
  category?: string;
  region?: string;
  limit?: number;
  page?: number;
}

export interface TrendAnalysis {
  trend_id: string;
  analysis: {
    popularity_score: number;
    growth_prediction: string;
    market_opportunity: string;
    competitor_analysis: string[];
    recommendations: string[];
  };
}

export interface UserPreferences {
  preferred_categories: string[];
  preferred_regions: string[];
  style_preferences: string[];
  budget_range: string;
  sustainability_importance: number;
} 