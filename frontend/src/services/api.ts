import axios from 'axios';
import { TrendsResponse, SearchParams, TrendAnalysis, UserPreferences } from '../types/fashion';

// Use environment variable for API URL, fallback to deployed backend for production
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://fashioning-ai-backend-818105867641.us-central1.run.app/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Add request interceptor for better error handling
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    if (error.code === 'ECONNREFUSED') {
      console.error('Backend server is not running. Please start the backend server.');
    }
    return Promise.reject(error);
  }
);

// Fallback data for when API is not available
const fallbackTrends: TrendsResponse = {
  success: true,
  data: {
    hits: [
      {
        objectID: "demo_1",
        name: "Sustainable Luxury Fashion",
        category: "luxury",
        description: "High-end fashion brands embracing eco-friendly materials and ethical production methods",
        regions: ["Global"],
        brand: "Stella McCartney",
        source: "Vogue Runway",
        trend_score: 0.92,
        growth_rate: 22.8,
        color_palette: ["#228B22", "#8B4513", "#F5F5DC"],
        demographics: {
          primary_age: "26-35",
          secondary_age: "36-45",
          gender_split: { female: 70, male: 30 }
        },
        sustainability_score: 0.95,
        predicted_peak: "2025-10-23T00:40:30.557922",
        social_mentions: 28750,
        influencer_adoptions: 156,
        brand_adoptions: ["Stella McCartney", "Patagonia", "Eileen Fisher"],
        tags: [],
        created_at: "2025-07-25T00:40:30.557922",
        updated_at: "2025-07-25T00:40:30.557922"
      },
      {
        objectID: "demo_2",
        name: "Y2K Revival Streetwear",
        category: "streetwear",
        description: "Early 2000s fashion making a comeback with metallic fabrics and futuristic accessories",
        regions: ["North America", "Europe"],
        brand: "Nike",
        source: "Vogue Runway",
        trend_score: 0.85,
        growth_rate: 15.2,
        color_palette: ["#C0C0C0", "#FF1493", "#00FFFF"],
        demographics: {
          primary_age: "18-25",
          secondary_age: "26-35",
          gender_split: { female: 60, male: 40 }
        },
        sustainability_score: 0.6,
        predicted_peak: "2025-09-23T00:40:30.557922",
        social_mentions: 15420,
        influencer_adoptions: 89,
        brand_adoptions: ["Nike", "Adidas", "Urban Outfitters"],
        tags: [],
        created_at: "2025-07-25T00:40:30.557922",
        updated_at: "2025-07-25T00:40:30.557922"
      }
    ],
    total: 2,
    page: 0,
    pages: 1,
    facets: {},
    processing_time: 0.1
  },
  message: "Demo data loaded (backend not available)"
};

const fallbackCategories = ["luxury", "streetwear", "sustainable", "casual", "formal", "vintage", "minimalist", "maximalist", "athleisure", "avant-garde"];
const fallbackRegions = ["Global", "North America", "Europe", "Asia Pacific", "Australia", "Africa"];

export const fashionApi = {
  // Get trending fashion items with optional filters
  getTrends: async (params: SearchParams = {}): Promise<TrendsResponse> => {
    try {
      const response = await api.get('/trends/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching trends from backend:', error);
      // Only use fallback if backend is completely unavailable
      if (error.code === 'ECONNREFUSED' || error.response?.status >= 500) {
        console.warn('Backend unavailable, using fallback data');
        return fallbackTrends;
      }
      throw error;
    }
  },

  // Search trends with query
  searchTrends: async (query: string, params: SearchParams = {}): Promise<TrendsResponse> => {
    try {
      const response = await api.get('/trends/', { 
        params: { query: query, ...params } 
      });
      return response.data;
    } catch (error) {
      console.error('Error searching trends from backend:', error);
      // Only use fallback if backend is completely unavailable
      if (error.code === 'ECONNREFUSED' || error.response?.status >= 500) {
        console.warn('Backend unavailable, using fallback data for search');
        // Filter fallback data based on query
        const filteredHits = fallbackTrends.data.hits.filter(trend => 
          trend.name.toLowerCase().includes(query.toLowerCase()) ||
          trend.description.toLowerCase().includes(query.toLowerCase()) ||
          trend.category.toLowerCase().includes(query.toLowerCase())
        );
        return {
          ...fallbackTrends,
          data: {
            ...fallbackTrends.data,
            hits: filteredHits,
            total: filteredHits.length
          }
        };
      }
      throw error;
    }
  },

  // Get personalized trends based on user preferences
  getPersonalizedTrends: async (preferences: UserPreferences): Promise<TrendsResponse> => {
    try {
      const response = await api.post('/trends/personalized', preferences);
      return response.data;
    } catch (error) {
      console.warn('Using fallback data for personalized trends');
      return fallbackTrends;
    }
  },

  // Get trend analysis
  getTrendAnalysis: async (trendId: string): Promise<TrendAnalysis> => {
    try {
      const response = await api.get(`/trends/${trendId}/analysis`);
      return response.data;
    } catch (error) {
      console.warn('Using fallback data for trend analysis');
      return {
        trend_id: trendId,
        analysis: {
          popularity_score: 0.8,
          growth_prediction: "Strong growth expected",
          market_opportunity: "High market potential",
          competitor_analysis: ["Competitor A", "Competitor B"],
          recommendations: ["Focus on sustainability", "Target younger demographics"]
        }
      };
    }
  },

  // Get available categories
  getCategories: async (): Promise<string[]> => {
    try {
      const response = await api.get('/trends/categories');
      return response.data;
    } catch (error) {
      console.error('Error fetching categories from backend:', error);
      // Only use fallback if backend is completely unavailable
      if (error.code === 'ECONNREFUSED' || error.response?.status >= 500) {
        console.warn('Backend unavailable, using fallback categories');
        return fallbackCategories;
      }
      throw error;
    }
  },

  // Get available regions
  getRegions: async (): Promise<string[]> => {
    try {
      const response = await api.get('/trends/regions');
      return response.data;
    } catch (error) {
      console.error('Error fetching regions from backend:', error);
      // Only use fallback if backend is completely unavailable
      if (error.code === 'ECONNREFUSED' || error.response?.status >= 500) {
        console.warn('Backend unavailable, using fallback regions');
        return fallbackRegions;
      }
      throw error;
    }
  },

  // Get fashion products related to a trend
  getFashionProducts: async (trendId: string, params: any = {}): Promise<any> => {
    try {
      const response = await api.get(`/trends/${trendId}/products`, { params });
      return response.data;
    } catch (error) {
      console.warn('Using fallback data for products');
      return {
        success: true,
        data: {
          products: [],
          total: 0
        },
        message: "Demo data (backend not available)"
      };
    }
  },

  // Get combined statistics from both indices
  getCombinedStats: async (): Promise<any> => {
    try {
      const response = await api.get('/trends/stats/combined');
      if (response.data && response.data.success) {
        return response.data.data;
      }
      throw new Error(response.data.message || 'Failed to fetch stats');
    } catch (error) {
      console.error('Error fetching combined stats:', error);
      // Return fallback stats
      return {
        trends_total: 5,
        news_total: 0,
        categories: 10,
        regions: 7
      };
    }
  },

  // Search fashion news
  searchNews: async (query: string = "", params: any = {}): Promise<any> => {
    try {
      const response = await api.get('/news/search', { 
        params: { query, ...params } 
      });
      return response.data;
    } catch (error) {
      console.error('Error searching news:', error);
      return {
        hits: [],
        total: 0,
        page: 0,
        pages: 0,
        processing_time: 0
      };
    }
  },

  // AI Chat Functions
  chatWithAI: async (chatRequest: { message: string; context?: any }): Promise<any> => {
    try {
      const response = await api.post('/ai/chat', chatRequest);
      return response.data;
    } catch (error) {
      console.error('Error chatting with AI:', error);
      throw error;
    }
  },

  comprehensiveAnalysis: async (trendId: string): Promise<any> => {
    try {
      const response = await api.post('/ai/comprehensive-analysis', { trend_id: trendId });
      return response.data;
    } catch (error) {
      console.error('Error getting comprehensive analysis:', error);
      throw error;
    }
  },

  // Data Enrichment Functions
  enrichTrends: async (request: { sources?: string[]; categories?: string[]; regions?: string[]; force_refresh?: boolean }): Promise<any> => {
    try {
      const response = await api.post('/enrichment/enrich-trends', request);
      return response.data;
    } catch (error) {
      console.error('Error enriching trends:', error);
      throw error;
    }
  },

  getEnrichmentStatus: async (): Promise<any> => {
    try {
      const response = await api.get('/enrichment/enrichment-status');
      return response.data;
    } catch (error) {
      console.error('Error getting enrichment status:', error);
      throw error;
    }
  },

  getScrapedSources: async (): Promise<any> => {
    try {
      const response = await api.get('/enrichment/scraped-sources');
      return response.data;
    } catch (error) {
      console.error('Error getting scraped sources:', error);
      throw error;
    }
  },

  getEnrichmentAnalytics: async (): Promise<any> => {
    try {
      const response = await api.get('/enrichment/enrichment-analytics');
      return response.data;
    } catch (error) {
      console.error('Error getting enrichment analytics:', error);
      throw error;
    }
  },

  analyzeTrendWithAI: async (trendId: string): Promise<any> => {
    try {
      const response = await api.post('/ai/analyze-trend', { trend_id: trendId });
      return response.data;
    } catch (error) {
      console.error('Error analyzing trend with AI:', error);
      throw error;
    }
  },

  getStyleRecommendations: async (preferences: any = {}): Promise<any> => {
    try {
      const response = await api.post('/ai/style-recommendations', {
        user_preferences: preferences,
        include_trends: true,
        limit: 5
      });
      return response.data;
    } catch (error) {
      console.error('Error getting style recommendations:', error);
      throw error;
    }
  },

  predictFutureTrends: async (): Promise<any> => {
    try {
      const response = await api.get('/ai/predict-trends');
      return response.data;
    } catch (error) {
      console.error('Error predicting future trends:', error);
      throw error;
    }
  },

  getAISuggestions: async (): Promise<any> => {
    try {
      const response = await api.get('/ai/suggestions');
      return response.data;
    } catch (error) {
      console.error('Error getting AI suggestions:', error);
      return {
        data: {
          suggestions: [
            "Analyze the top trending fashion item",
            "What style would suit me for summer?",
            "Predict what will be popular next season",
            "How can I incorporate sustainable fashion?"
          ],
          categories: ["Trend Analysis", "Style Advice", "Future Predictions"]
        }
      };
    }
  },
};

export default api; 