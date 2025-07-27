import React, { useState, useEffect } from 'react';
import { TrendingUp, Tag, Globe } from 'lucide-react';
import { fashionApi } from '../services/api';

interface QuickStatsProps {
  className?: string;
}

const QuickStats: React.FC<QuickStatsProps> = ({ className = '' }) => {
  const [stats, setStats] = useState({
    totalTrends: 0,
    categories: 0,
    regions: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch combined stats from backend
      const statsResponse = await fashionApi.getCombinedStats();
      
      setStats({
        totalTrends: statsResponse.trends_total,
        categories: statsResponse.categories,
        regions: statsResponse.regions
      });
    } catch (err) {
      console.error('Error loading stats:', err);
      setError('Failed to load stats');
      // Set fallback values
      setStats({
        totalTrends: 5,
        categories: 10,
        regions: 7
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={`card p-6 ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Total Trends</span>
            <div className="w-8 h-4 bg-gray-200 rounded animate-pulse"></div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Categories</span>
            <div className="w-6 h-4 bg-gray-200 rounded animate-pulse"></div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Regions</span>
            <div className="w-6 h-4 bg-gray-200 rounded animate-pulse"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`card p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-gray-600">Total Trends</span>
          <span className="font-semibold text-gray-900">{stats.totalTrends}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-gray-600">Categories</span>
          <span className="font-semibold text-gray-900">{stats.categories}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-gray-600">Regions</span>
          <span className="font-semibold text-gray-900">{stats.regions}</span>
        </div>
      </div>
      {error && (
        <div className="mt-4 text-xs text-red-500">
          {error} - Showing demo data
        </div>
      )}
    </div>
  );
};

export default QuickStats; 