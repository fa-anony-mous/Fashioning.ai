import React, { useState, useEffect } from 'react';
import { TrendingUp, Leaf, DollarSign, Palette, Clock, Star, Loader2 } from 'lucide-react';
import { fashionApi } from '../services/api';
import { FashionTrend } from '../types/fashion';

interface ComprehensiveAnalysisProps {
  trend: FashionTrend;
  onClose: () => void;
}

interface AnalysisData {
  trend_name: string;
  popularity_analysis: string;
  sustainability_insights: string;
  market_opportunity: string;
  styling_guide: string;
  trend_lifespan: string;
  comprehensive_score: {
    overall_score: number;
    popularity_score: number;
    growth_score: number;
    sustainability_score: number;
    analysis_quality: number;
    trend_confidence: string;
  };
}

const ComprehensiveAnalysis: React.FC<ComprehensiveAnalysisProps> = ({ trend, onClose }) => {
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'popularity' | 'sustainability' | 'market' | 'styling' | 'lifespan'>('overview');

  useEffect(() => {
    fetchComprehensiveAnalysis();
  }, [trend]);

  const fetchComprehensiveAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fashionApi.comprehensiveAnalysis(trend.objectID);
      setAnalysis(response.data.comprehensive_analysis);
    } catch (err) {
      setError('Failed to load comprehensive analysis');
      console.error('Error fetching comprehensive analysis:', err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence.toLowerCase()) {
      case 'high': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
          <div className="flex items-center justify-center space-x-2">
            <Loader2 className="w-6 h-6 animate-spin text-primary-600" />
            <span className="text-lg font-medium">Analyzing trend with advanced AI...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
          <div className="text-center">
            <div className="text-red-600 mb-4">⚠️ {error}</div>
            <button
              onClick={onClose}
              className="btn-primary"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!analysis) return null;

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Star },
    { id: 'popularity', label: 'Popularity', icon: TrendingUp },
    { id: 'sustainability', label: 'Sustainability', icon: Leaf },
    { id: 'market', label: 'Market', icon: DollarSign },
    { id: 'styling', label: 'Styling', icon: Palette },
    { id: 'lifespan', label: 'Lifespan', icon: Clock },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="card p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Star className="w-5 h-5 text-primary-600" />
                  <span className="font-semibold">Overall Score</span>
                </div>
                <div className={`text-2xl font-bold ${getScoreColor(analysis.comprehensive_score.overall_score)}`}>
                  {analysis.comprehensive_score.overall_score}/100
                </div>
              </div>
              
              <div className="card p-4">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-5 h-5 text-green-600" />
                  <span className="font-semibold">Popularity</span>
                </div>
                <div className={`text-2xl font-bold ${getScoreColor(analysis.comprehensive_score.popularity_score)}`}>
                  {analysis.comprehensive_score.popularity_score}/100
                </div>
              </div>
              
              <div className="card p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Leaf className="w-5 h-5 text-green-600" />
                  <span className="font-semibold">Sustainability</span>
                </div>
                <div className={`text-2xl font-bold ${getScoreColor(analysis.comprehensive_score.sustainability_score)}`}>
                  {analysis.comprehensive_score.sustainability_score}/100
                </div>
              </div>
            </div>
            
            <div className="card p-6">
              <h3 className="text-lg font-semibold mb-4">Trend Confidence</h3>
              <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getConfidenceColor(analysis.comprehensive_score.trend_confidence)}`}>
                {analysis.comprehensive_score.trend_confidence} Confidence
              </div>
            </div>
          </div>
        );
      
      case 'popularity':
        return (
          <div className="card p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-primary-600" />
              Popularity Analysis
            </h3>
            <div className="prose max-w-none">
              <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                {analysis.popularity_analysis}
              </div>
            </div>
          </div>
        );
      
      case 'sustainability':
        return (
          <div className="card p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Leaf className="w-5 h-5 text-green-600" />
              Sustainability Insights
            </h3>
            <div className="prose max-w-none">
              <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                {analysis.sustainability_insights}
              </div>
            </div>
          </div>
        );
      
      case 'market':
        return (
          <div className="card p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-green-600" />
              Market Opportunity
            </h3>
            <div className="prose max-w-none">
              <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                {analysis.market_opportunity}
              </div>
            </div>
          </div>
        );
      
      case 'styling':
        return (
          <div className="card p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Palette className="w-5 h-5 text-purple-600" />
              Styling Guide
            </h3>
            <div className="prose max-w-none">
              <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                {analysis.styling_guide}
              </div>
            </div>
          </div>
        );
      
      case 'lifespan':
        return (
          <div className="card p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Clock className="w-5 h-5 text-blue-600" />
              Trend Lifespan Prediction
            </h3>
            <div className="prose max-w-none">
              <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                {analysis.trend_lifespan}
              </div>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-6xl w-full mx-4 max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-xl font-bold text-gray-900">Comprehensive Analysis</h2>
            <p className="text-sm text-gray-600">{trend.name}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-primary-600 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default ComprehensiveAnalysis; 