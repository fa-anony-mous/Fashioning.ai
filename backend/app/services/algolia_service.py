"""
Algolia Search Service for Fashion Trends
Core service for integrating with Algolia to fetch and analyze fashion trends
"""

import os
from algoliasearch.search_client import SearchClient
from app.core.config import settings
from typing import Dict, List, Optional, Any
from app.models.trend import Trend, TrendResponse
from app.services.mock_data import (
    get_mock_trends_response, 
    get_mock_categories, 
    get_mock_regions,
    get_mock_trend_by_id
)
from fastapi.concurrency import run_in_threadpool


class AlgoliaService:
    """Service for interacting with Algolia search API"""
    
    def __init__(self):
        """Initialize Algolia client"""
        if not settings.ALGOLIA_APP_ID or not settings.ALGOLIA_ADMIN_API_KEY:
            self.client = None
            return
            
        self.client = SearchClient.create(
            settings.ALGOLIA_APP_ID,
            settings.ALGOLIA_ADMIN_API_KEY
        )
        # Support multiple indices
        self.trends_index_name = os.getenv("ALGOLIA_TRENDS_INDEX", "fashion_trends")
        self.news_index_name = os.getenv("ALGOLIA_NEWS_INDEX", "fashion_news")

    async def search_trends(
        self, query: str = "", limit: int = 20, offset: int = 0, 
        category: Optional[str] = None, region: Optional[str] = None
    ) -> TrendResponse:
        """
        Search for fashion trends using Algolia, with optional filters.
        """
        if not self.client:
            return get_mock_trends_response()
            
        filters = []
        if category:
            filters.append(f"category:'{category}'")
        if region:
            filters.append(f"regions:'{region}'")
        filter_string = " AND ".join(filters)

        try:
            trends_index = self.client.init_index(self.trends_index_name)
            
            response = await run_in_threadpool(
                trends_index.search,
                query,
                {
                    "hitsPerPage": limit,
                    "page": offset // limit if limit > 0 else 0,
                    "filters": filter_string,
                    "facets": ["category", "regions"]
                }
            )

            hits = [Trend(**dict(hit)) for hit in response.get("hits", [])]
            
            trend_response = TrendResponse(
                hits=hits,
                total=response.get("nbHits", 0),
                limit=limit,
                offset=offset,
                pages=response.get("nbPages", 0),
                facets=response.get("facets", {}),
                processing_time=response.get("processingTimeMS", 0)
            )
            return trend_response
        except Exception as e:
            return get_mock_trends_response()
    
    async def get_trend_by_id(self, trend_id: str) -> Optional[Trend]:
        """
        Retrieve a single trend by its objectID.
        """
        if not self.client:
            return get_mock_trend_by_id(trend_id)
        
        try:
            trends_index = self.client.init_index(self.trends_index_name)
            response = await run_in_threadpool(trends_index.get_object, trend_id)
            return Trend(**response)
        except Exception as e:
            return get_mock_trend_by_id(trend_id)

    async def get_facet_values(self, facet_name: str) -> List[str]:
        """
        Get all unique values for a given facet from the Algolia index.
        """
        if not self.client:
            if facet_name == 'category':
                return get_mock_categories()
            elif facet_name == 'regions':
                return get_mock_regions()
            return []
        
        try:
            trends_index = self.client.init_index(self.trends_index_name)
            response = await run_in_threadpool(trends_index.search_for_facet_values, facet_name, "")
            return [facet['value'] for facet in response.get("facetHits", [])]
        except Exception:
            if facet_name == 'category':
                return get_mock_categories()
            elif facet_name == 'regions':
                return get_mock_regions()
            return []

    async def search_news(self, query: str = "", page: int = 0, per_page: int = 20) -> Dict[str, Any]:
        """
        Search fashion news from the fashion_news index.
        """
        if not self.client:
            return {"hits": [], "total": 0, "page": page, "pages": 0, "processing_time": 0}
        
        try:
            news_index = self.client.init_index(self.news_index_name)
            response = await run_in_threadpool(
                news_index.search,
                query,
                {"page": page, "hitsPerPage": per_page, "attributesToHighlight": []}
            )
            
            return {
                "hits": response.get("hits", []),
                "total": response.get("nbHits", 0),
                "page": response.get("page", 0),
                "pages": response.get("nbPages", 0),
                "processing_time": response.get("processingTimeMS", 0)
            }
        except Exception as e:
            print(f"Algolia news search error: {e}")
            return {"hits": [], "total": 0, "page": page, "pages": 0, "processing_time": 0}

    async def get_all_categories(self) -> List[str]:
        if not self.client:
            return get_mock_categories()

        try:
            trends_index = self.client.init_index(self.trends_index_name)
            response = await run_in_threadpool(trends_index.search, "", {"facets": ["category"]})
            return list(response.get("facets", {}).get("category", {}).keys())
        except Exception as e:
            return get_mock_categories()

    async def get_all_regions(self) -> List[str]:
        if not self.client:
            return get_mock_regions()
            
        try:
            trends_index = self.client.init_index(self.trends_index_name)
            response = await run_in_threadpool(trends_index.search, "", {"facets": ["regions"]})
            return list(response.get("facets", {}).get("regions", {}).keys())
        except Exception as e:
            return get_mock_regions()

    async def get_combined_stats(self) -> Dict[str, Any]:
        """
        Get combined statistics from both indices.
        """
        if not self.client:
            return {
                "trends_total": 3,
                "categories": 3,
                "regions": 3,
            }
        try:
            trends_index = self.client.init_index(self.trends_index_name)
            # Use search to get total counts from facets
            response = await run_in_threadpool(trends_index.search, '', {
                'hitsPerPage': 0,
                'facets': ['category', 'regions']
            })
            
            return {
                "trends_total": response.get('nbHits', 0),
                "categories": len(response.get('facets', {}).get('category', {})),
                "regions": len(response.get('facets', {}).get('regions', {})),
            }
        except Exception as e:
            return {
                "trends_total": 3,
                "categories": 3,
                "regions": 3,
            }
            
    async def close(self):
        """Close the Algolia async client."""
        if self.client:
            await run_in_threadpool(self.client.close)

# Singleton instance of the service
algolia_service = AlgoliaService()