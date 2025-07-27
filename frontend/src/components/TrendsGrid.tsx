import React, { useState, useEffect } from 'react';
import { Loader2, AlertCircle, RefreshCw } from 'lucide-react';
import { FashionTrend } from '../types/fashion';
import { fashionApi } from '../services/api';
import TrendCard from './TrendCard';

interface TrendsGridProps {
  filters: { category?: string; region?: string; query?: string };
  onTrendClick?: (trend: FashionTrend) => void;
  onComprehensiveAnalysis?: (trend: FashionTrend) => void;
}

const TrendsGrid: React.FC<TrendsGridProps> = ({ filters, onTrendClick, onComprehensiveAnalysis }) => {
  const [trends, setTrends] = useState<FashionTrend[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    loadTrends();
  }, [filters.category, filters.region, filters.query]);

  const loadTrends = async () => {
    setLoading(true);
    setError(null);
    
    try {
      let response;
      
      if (filters.query) {
        response = await fashionApi.searchTrends(filters.query, {
          category: filters.category,
          region: filters.region,
          limit: 20,
        });
      } else {
        response = await fashionApi.getTrends({
          category: filters.category,
          region: filters.region,
          limit: 20,
        });
      }
      
      if (!response) {
        throw new Error('No response received from API');
      }
      
      if (!response.hits) {
        throw new Error('Response missing hits array');
      }
      
      setTrends(response.hits);
      setTotal(response.total);
    } catch (err) {
      console.error('Error loading trends:', err);
      setError('Failed to load fashion trends. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    loadTrends();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Loader2 className="w-8 h-8 text-primary-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading fashion trends...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Something went wrong</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={handleRetry}
            className="btn-primary flex items-center gap-2 mx-auto"
          >
            <RefreshCw className="w-4 h-4" />
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (trends.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">👗</span>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No trends found</h3>
          <p className="text-gray-600 mb-4">
            Try adjusting your filters or search terms
          </p>
          <button
            onClick={() => window.location.reload()}
            className="btn-secondary"
          >
            View All Trends
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Results Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Fashion Trends
          </h2>
          <p className="text-gray-600">
            Found {total} trending fashion items
          </p>
        </div>
        <button
          onClick={handleRetry}
          className="btn-secondary flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Trends Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {trends.map((trend) => (
          <TrendCard
            key={trend.objectID}
            trend={trend}
            onClick={onTrendClick}
            onComprehensiveAnalysis={onComprehensiveAnalysis}
          />
        ))}
      </div>

      {/* Load More Button (if needed) */}
      {trends.length < total && (
        <div className="text-center pt-8">
          <button className="btn-primary">
            Load More Trends
          </button>
        </div>
      )}
    </div>
  );
};

export default TrendsGrid; 