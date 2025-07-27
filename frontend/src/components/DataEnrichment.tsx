import React, { useState, useEffect } from 'react';
import { RefreshCw, Database, TrendingUp, Globe, Clock, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { fashionApi } from '../services/api';

interface DataEnrichmentProps {
  isOpen: boolean;
  onClose: () => void;
}

interface SourceInfo {
  description: string;
  data_type: string;
  unique_value: string;
  categories: string[];
  update_frequency: string;
}

interface EnrichmentStatus {
  status: string;
  last_enrichment: string;
  total_trends_enriched: number;
  sources_processed: number;
  next_scheduled: string;
}

const DataEnrichment: React.FC<DataEnrichmentProps> = ({ isOpen, onClose }) => {
  const [sources, setSources] = useState<Record<string, SourceInfo>>({});
  const [status, setStatus] = useState<EnrichmentStatus | null>(null);
  const [analytics, setAnalytics] = useState<any>(null);
  const [isEnriching, setIsEnriching] = useState(false);
  const [selectedSources, setSelectedSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen]);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Load sources info
      const sourcesResponse = await fashionApi.getScrapedSources();
      setSources(sourcesResponse.data.sources);
      
      // Load enrichment status
      const statusResponse = await fashionApi.getEnrichmentStatus();
      setStatus(statusResponse.data);
      
      // Load analytics
      const analyticsResponse = await fashionApi.getEnrichmentAnalytics();
      setAnalytics(analyticsResponse.data);
      
    } catch (error) {
      console.error('Error loading enrichment data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEnrichment = async () => {
    try {
      setIsEnriching(true);
      
      const response = await fashionApi.enrichTrends({
        sources: selectedSources.length > 0 ? selectedSources : undefined,
        force_refresh: true
      });
      
      if (response.success) {
        // Poll for status updates
        setTimeout(() => {
          loadData();
        }, 2000);
      }
      
    } catch (error) {
      console.error('Error starting enrichment:', error);
    } finally {
      setIsEnriching(false);
    }
  };

  const toggleSource = (sourceName: string) => {
    setSelectedSources(prev => 
      prev.includes(sourceName) 
        ? prev.filter(s => s !== sourceName)
        : [...prev, sourceName]
    );
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed': return 'text-green-600 bg-green-100';
      case 'processing': return 'text-blue-600 bg-blue-100';
      case 'failed': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-6xl w-full mx-4 max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-xl font-bold text-gray-900">Data Enrichment</h2>
            <p className="text-sm text-gray-600">Enrich Algolia MCP with fashion data from multiple sources</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            ✕
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center p-8">
            <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
            <span className="ml-2">Loading enrichment data...</span>
          </div>
        ) : (
          <div className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
            {/* Status Overview */}
            {status && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div className="card p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Database className="w-5 h-5 text-primary-600" />
                    <span className="font-semibold">Status</span>
                  </div>
                  <div className={`inline-flex items-center px-2 py-1 rounded-full text-sm font-medium ${getStatusColor(status.status)}`}>
                    {status.status}
                  </div>
                </div>
                
                <div className="card p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                    <span className="font-semibold">Trends Enriched</span>
                  </div>
                  <div className="text-2xl font-bold text-green-600">
                    {status.total_trends_enriched}
                  </div>
                </div>
                
                <div className="card p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Globe className="w-5 h-5 text-blue-600" />
                    <span className="font-semibold">Sources</span>
                  </div>
                  <div className="text-2xl font-bold text-blue-600">
                    {status.sources_processed}
                  </div>
                </div>
                
                <div className="card p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Clock className="w-5 h-5 text-purple-600" />
                    <span className="font-semibold">Last Updated</span>
                  </div>
                  <div className="text-sm text-gray-600">
                    {new Date(status.last_enrichment).toLocaleDateString()}
                  </div>
                </div>
              </div>
            )}

            {/* Sources Selection */}
            <div className="card p-6 mb-6">
              <h3 className="text-lg font-semibold mb-4">Select Sources to Enrich</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(sources).map(([sourceName, sourceInfo]) => (
                  <div
                    key={sourceName}
                    className={`border-2 rounded-lg p-4 cursor-pointer transition-colors ${
                      selectedSources.includes(sourceName)
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => toggleSource(sourceName)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">{sourceName}</h4>
                      {selectedSources.includes(sourceName) && (
                        <CheckCircle className="w-5 h-5 text-primary-600" />
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{sourceInfo.description}</p>
                    <div className="text-xs text-gray-500">
                      <div>Type: {sourceInfo.data_type}</div>
                      <div>Frequency: {sourceInfo.update_frequency}</div>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-4 flex gap-2">
                <button
                  onClick={() => setSelectedSources(Object.keys(sources))}
                  className="btn-secondary text-sm"
                >
                  Select All
                </button>
                <button
                  onClick={() => setSelectedSources([])}
                  className="btn-secondary text-sm"
                >
                  Clear All
                </button>
              </div>
            </div>

            {/* Analytics */}
            {analytics && (
              <div className="card p-6 mb-6">
                <h3 className="text-lg font-semibold mb-4">Data Quality Analytics</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {Math.round(analytics.data_quality.completeness * 100)}%
                    </div>
                    <div className="text-sm text-gray-600">Completeness</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {Math.round(analytics.data_quality.freshness * 100)}%
                    </div>
                    <div className="text-sm text-gray-600">Freshness</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {Math.round(analytics.data_quality.accuracy * 100)}%
                    </div>
                    <div className="text-sm text-gray-600">Accuracy</div>
                  </div>
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={handleEnrichment}
                disabled={isEnriching}
                className="btn-primary flex items-center gap-2"
              >
                {isEnriching ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <RefreshCw className="w-4 h-4" />
                )}
                {isEnriching ? 'Enriching...' : 'Start Enrichment'}
              </button>
              
              <button
                onClick={loadData}
                className="btn-secondary flex items-center gap-2"
              >
                <RefreshCw className="w-4 h-4" />
                Refresh Status
              </button>
              
              <button
                onClick={onClose}
                className="btn-secondary"
              >
                Close
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DataEnrichment; 