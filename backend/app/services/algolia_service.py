"""
Algolia Search Service for Fashion Trends
Core service for integrating with Algolia to fetch and analyze fashion trends
"""

import os
from algoliasearch.search.client import SearchClient
from app.core.config import settings
from typing import Dict, List, Optional, Any
from app.models.trend import Trend, TrendResponse
from app.services.mock_data import (
    get_mock_trends_response, 
    get_mock_categories, 
    get_mock_regions,
    get_mock_trend_by_id
)

class AlgoliaService:
    """Service for interacting with Algolia search API"""
    
    def __init__(self):
        """Initialize Algolia client"""
        if not settings.ALGOLIA_APP_ID or not settings.ALGOLIA_ADMIN_API_KEY:
            self.client = None
            self.async_client = None
            return
            
        self.async_client = SearchClient(
            settings.ALGOLIA_APP_ID,
            settings.ALGOLIA_ADMIN_API_KEY
        )
        # Support multiple indices
        self.trends_index = os.getenv("ALGOLIA_TRENDS_INDEX", "fashion_trends")
        self.news_index = os.getenv("ALGOLIA_NEWS_INDEX", "fashion_news")
        self.index_name = self.trends_index  # Default for backward compatibility
    
    async def search_trends(
        self,
        query: str,
        category: Optional[str] = None,
        region: Optional[str] = None,
        page: int = 0,
        per_page: int = 20
    ) -> TrendResponse:
        """
        Search for fashion trends using Algolia, with optional filters.
        """
        if not self.async_client:
            # Use mock data when Algolia is not configured
            return get_mock_trends_response(query, category, region, page, per_page)
        
        filters = []
        if category:
            filters.append(f"category:'{category}'")
        if region:
            filters.append(f"regions:'{region}'")
        
        filter_string = " AND ".join(filters) if filters else ""
        
        try:
            response = await self.async_client.search_single_index(
                index_name=self.index_name,
                search_params={
                    "query": query,
                    "page": page,
                    "hitsPerPage": per_page,
                    "attributesToHighlight": [],
                    "filters": filter_string,
                    "facets": ["category", "regions"]
                }
            )
            
            hits = [Trend(**dict(hit)) for hit in response.hits]
            
            return TrendResponse(
                hits=hits,
                total=response.nb_hits,
                page=response.page,
                pages=response.nb_pages,
                facets=response.facets or {},
                processing_time=response.processing_time_ms
            )
        except Exception as e:
            # In case of an error, use mock data
            print(f"Algolia error: {e}, using mock data")
            return get_mock_trends_response(query, category, region, page, per_page)
    
    async def get_trend_by_id(self, trend_id: str) -> Optional[Trend]:
        """
        Retrieve a single trend by its objectID.
        """
        if not self.async_client:
            # Use mock data when Algolia is not configured
            return get_mock_trend_by_id(trend_id)
            
        try:
            response = await self.async_client.get_object(
                index_name=self.index_name,
                object_id=trend_id
            )
            return Trend(**response)
        except Exception:
            # Use mock data on error
            return get_mock_trend_by_id(trend_id)

    async def get_facet_values(self, facet_name: str) -> List[str]:
        """
        Get all unique values for a given facet from the Algolia index.
        """
        if not self.async_client:
            # Use mock data when Algolia is not configured
            if facet_name == 'category':
                return get_mock_categories()
            elif facet_name == 'regions':
                return get_mock_regions()
            return []
        
        try:
            response = await self.async_client.search_for_facet_values(
                index_name=self.trends_index,
                facet_name=facet_name,
                facet_query=""
            )
            return [facet.value for facet in response.facet_hits]
        except Exception:
            # Use mock data on error
            if facet_name == 'category':
                return get_mock_categories()
            elif facet_name == 'regions':
                return get_mock_regions()
            return []

    async def search_news(self, query: str = "", page: int = 0, per_page: int = 20) -> Dict[str, Any]:
        """
        Search fashion news from the fashion_news index.
        """
        if not self.async_client:
            return {
                "hits": [],
                "total": 0,
                "page": page,
                "pages": 0,
                "processing_time": 0
            }
        
        try:
            response = await self.async_client.search_single_index(
                index_name=self.news_index,
                search_params={
                    "query": query,
                    "page": page,
                    "hitsPerPage": per_page,
                    "attributesToHighlight": []
                }
            )
            
            return {
                "hits": response.hits,
                "total": response.nb_hits,
                "page": response.page,
                "pages": response.nb_pages,
                "processing_time": response.processing_time_ms
            }
        except Exception as e:
            print(f"Algolia news search error: {e}")
            return {
                "hits": [],
                "total": 0,
                "page": page,
                "pages": 0,
                "processing_time": 0
            }

    async def get_combined_stats(self) -> Dict[str, Any]:
        """
        Get combined statistics from both indices.
        """
        if not self.async_client:
            return {
                "trends_total": 5,
                "news_total": 0,
                "categories": len(get_mock_categories()),
                "regions": len(get_mock_regions())
            }
        
        try:
            # Get trends count
            trends_response = await self.async_client.search_single_index(
                index_name=self.trends_index,
                search_params={"query": "", "hitsPerPage": 1}
            )
            
            # Get news count
            news_response = await self.async_client.search_single_index(
                index_name=self.news_index,
                search_params={"query": "", "hitsPerPage": 1}
            )
            
            # Get categories and regions
            categories = await self.get_facet_values('category')
            regions = await self.get_facet_values('regions')
            
            return {
                "trends_total": trends_response.nb_hits,
                "news_total": news_response.nb_hits,
                "categories": len(categories),
                "regions": len(regions)
            }
        except Exception as e:
            print(f"Error getting combined stats: {e}")
            return {
                "trends_total": 5,
                "news_total": 0,
                "categories": len(get_mock_categories()),
                "regions": len(get_mock_regions())
            }

    async def close(self):
        """Close the Algolia async client."""
        if self.async_client:
            await self.async_client.close()

# Create global instance
algolia_service = AlgoliaService()