import React from 'react';
import { FashionTrend } from '../types/fashion';
import { TrendingUp, MapPin, Users, Star, Calendar, Sparkles } from 'lucide-react';

interface TrendCardProps {
  trend: FashionTrend;
  onClick?: (trend: FashionTrend) => void;
  onComprehensiveAnalysis?: (trend: FashionTrend) => void;
}

const TrendCard: React.FC<TrendCardProps> = ({ trend, onClick, onComprehensiveAnalysis }) => {
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      luxury: 'bg-gradient-to-r from-fashion-gold to-yellow-400',
      streetwear: 'bg-gradient-to-r from-gray-800 to-gray-600',
      sustainable: 'bg-gradient-to-r from-green-500 to-emerald-400',
      vintage: 'bg-gradient-to-r from-amber-600 to-orange-500',
      minimalist: 'bg-gradient-to-r from-gray-400 to-gray-300',
      maximalist: 'bg-gradient-to-r from-fashion-purple to-pink-500',
      athleisure: 'bg-gradient-to-r from-blue-500 to-cyan-400',
      formal: 'bg-gradient-to-r from-slate-700 to-slate-500',
      casual: 'bg-gradient-to-r from-blue-400 to-indigo-500',
      'avant-garde': 'bg-gradient-to-r from-fashion-rose to-purple-600',
    };
    return colors[category.toLowerCase()] || 'bg-gradient-to-r from-gray-500 to-gray-400';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getImageUrl = () => {
    return trend.image_url || (trend.images && trend.images[0]) || null;
  };

  return (
    <div 
      className="trend-card group"
      onClick={() => onClick?.(trend)}
    >
      {/* Image Section */}
      <div className="relative h-48 overflow-hidden">
        {getImageUrl() ? (
          <img
            src={getImageUrl()}
            alt={trend.name}
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
            <div className="text-center text-gray-500">
              <div className="w-16 h-16 mx-auto mb-2 bg-gray-400 rounded-full flex items-center justify-center">
                <span className="text-2xl">👗</span>
              </div>
              <p className="text-sm">No Image</p>
            </div>
          </div>
        )}
        
        {/* Category Badge */}
        <div className={`absolute top-3 left-3 px-3 py-1 rounded-full text-white text-xs font-medium ${getCategoryColor(trend.category)}`}>
          {trend.category}
        </div>
        
        {/* Trend Score Badge */}
        <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full text-xs font-medium text-gray-700 flex items-center gap-1">
          <Star className="w-3 h-3 text-yellow-500 fill-current" />
          {trend.trend_score.toFixed(1)}
        </div>
      </div>

      {/* Content Section */}
      <div className="p-4">
        {/* Title */}
        <h3 className="font-fashion text-lg font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
          {trend.name}
        </h3>
        
        {/* Description */}
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {trend.description}
        </p>
        
        {/* Stats Row */}
        <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
          <div className="flex items-center gap-1">
            <TrendingUp className="w-3 h-3" />
            <span>{trend.growth_rate}% growth</span>
          </div>
          <div className="flex items-center gap-1">
            <Users className="w-3 h-3" />
            <span>{trend.social_mentions.toLocaleString()}</span>
          </div>
        </div>
        
        {/* Regions */}
        <div className="flex items-center gap-1 text-xs text-gray-500 mb-3">
          <MapPin className="w-3 h-3" />
          <span>{trend.regions.join(', ')}</span>
        </div>
        
        {/* Bottom Row */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Calendar className="w-3 h-3" />
            <span>Peak: {formatDate(trend.predicted_peak)}</span>
          </div>
          
          {/* Sustainability Score */}
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full bg-green-500"></div>
            <span className="text-xs text-gray-500">
              {Math.round(trend.sustainability_score * 100)}% sustainable
            </span>
          </div>
        </div>
        
        {/* Action Buttons */}
        <div className="flex gap-2 mt-3">
          <button
            onClick={(e) => {
              e.stopPropagation();
              onComprehensiveAnalysis?.(trend);
            }}
            className="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs px-3 py-2 rounded-lg font-medium hover:from-purple-600 hover:to-pink-600 transition-colors flex items-center justify-center gap-1"
          >
            <Sparkles className="w-3 h-3" />
            Deep Analysis
          </button>
        </div>
      </div>
    </div>
  );
};

export default TrendCard; 