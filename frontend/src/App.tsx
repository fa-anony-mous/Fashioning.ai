import { useState } from 'react';
import { Sparkles, Heart, TrendingUp, Globe, MessageCircle, Database } from 'lucide-react';
import type { FashionTrend } from './types/fashion';
import SearchFilters from './components/SearchFilters';
import TrendsGrid from './components/TrendsGrid';
import QuickStats from './components/QuickStats';
import AIChat from './components/AIChat';
import ComprehensiveAnalysis from './components/ComprehensiveAnalysis';
import DataEnrichment from './components/DataEnrichment';

function App() {
  const [filters, setFilters] = useState<{ category?: string; region?: string; query?: string }>({});
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatContext, setChatContext] = useState<any>(null);
  const [resetChat, setResetChat] = useState(false);
  const [activeView, setActiveView] = useState<'trends' | 'global' | 'favorites'>('trends');
  const [comprehensiveAnalysisTrend, setComprehensiveAnalysisTrend] = useState<FashionTrend | null>(null);
  const [isDataEnrichmentOpen, setIsDataEnrichmentOpen] = useState(false);

  const handleFiltersChange = (newFilters: { category?: string; region?: string; query?: string }) => {
    setFilters(newFilters);
  };

  const handleTrendClick = (trend: FashionTrend) => {
    // Set the trend as context for AI chat and reset chat
    setChatContext({ trends: [trend] });
    setResetChat(true);
    setIsChatOpen(true);
    
    // Reset the resetChat flag after a brief delay
    setTimeout(() => setResetChat(false), 100);
  };

  const openAIChat = () => {
    // Open general chat without resetting
    setChatContext(null);
    setIsChatOpen(true);
  };

  const closeAIChat = () => {
    setIsChatOpen(false);
  };

  const handleComprehensiveAnalysis = (trend: FashionTrend) => {
    setComprehensiveAnalysisTrend(trend);
  };

  const closeComprehensiveAnalysis = () => {
    setComprehensiveAnalysisTrend(null);
  };

  const handleNavigation = (view: 'trends' | 'global' | 'favorites') => {
    setActiveView(view);
    // Reset filters when switching views
    setFilters({});
  };

  const renderMainContent = () => {
    switch (activeView) {
      case 'trends':
        return <TrendsGrid filters={filters} onTrendClick={handleTrendClick} onComprehensiveAnalysis={handleComprehensiveAnalysis} />;
      case 'global':
        return (
          <div className="card p-8 text-center">
            <Globe className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Global Fashion Insights</h2>
            <p className="text-gray-600 mb-6">Discover fashion trends from around the world</p>
            <TrendsGrid filters={{ ...filters, region: 'global' }} onTrendClick={handleTrendClick} onComprehensiveAnalysis={handleComprehensiveAnalysis} />
          </div>
        );
      case 'favorites':
        return (
          <div className="card p-8 text-center">
            <Heart className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Your Favorites</h2>
            <p className="text-gray-600 mb-6">Save and organize your favorite fashion trends</p>
            <div className="text-gray-500">
              <p>Favorites feature coming soon!</p>
              <p className="text-sm mt-2">Click on trends to save them to your favorites</p>
            </div>
          </div>
        );
      default:
        return <TrendsGrid filters={filters} onTrendClick={handleTrendClick} onComprehensiveAnalysis={handleComprehensiveAnalysis} />;
    }
  };

  return (
    <div className="min-h-screen gradient-bg">
      {/* Header */}
      <header className="glass-effect sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 fashion-gradient rounded-xl flex items-center justify-center shadow-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gradient font-fashion">
                  Fashioning.ai
                </h1>
                <p className="text-xs text-gray-500">AI-Powered Fashion Trends</p>
              </div>
            </div>
            
            <nav className="hidden md:flex items-center gap-6">
              <button 
                onClick={() => handleNavigation('trends')}
                className={`flex items-center gap-2 transition-colors font-medium ${
                  activeView === 'trends' 
                    ? 'text-primary-600' 
                    : 'text-gray-600 hover:text-primary-600'
                }`}
              >
                <TrendingUp className="w-4 h-4" />
                <span>Trends</span>
              </button>
              <button 
                onClick={() => handleNavigation('global')}
                className={`flex items-center gap-2 transition-colors font-medium ${
                  activeView === 'global' 
                    ? 'text-primary-600' 
                    : 'text-gray-600 hover:text-primary-600'
                }`}
              >
                <Globe className="w-4 h-4" />
                <span>Global</span>
              </button>
              <button 
                onClick={() => handleNavigation('favorites')}
                className={`flex items-center gap-2 transition-colors font-medium ${
                  activeView === 'favorites' 
                    ? 'text-primary-600' 
                    : 'text-gray-600 hover:text-primary-600'
                }`}
              >
                <Heart className="w-4 h-4" />
                <span>Favorites</span>
              </button>
            </nav>

            <div className="flex items-center gap-3">
              <button 
                onClick={() => setIsDataEnrichmentOpen(true)}
                className="btn-secondary flex items-center gap-2 shadow-md"
              >
                <Database className="w-4 h-4" />
                <span className="hidden sm:inline">Enrich Data</span>
              </button>
              <button 
                onClick={openAIChat}
                className="btn-secondary flex items-center gap-2 shadow-md"
              >
                <Sparkles className="w-4 h-4" />
                <span className="hidden sm:inline">Ask AI</span>
              </button>
              <button className="btn-primary shadow-md">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <SearchFilters onFiltersChange={handleFiltersChange} />
            
            {/* Quick Stats */}
            <QuickStats />

            {/* Featured Categories */}
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Featured Categories</h3>
              <div className="space-y-2">
                {['Luxury', 'Streetwear', 'Sustainable', 'Vintage'].map((category) => (
                  <button
                    key={category}
                    className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 transition-colors text-gray-700 hover:text-primary-600"
                    onClick={() => handleFiltersChange({ category: category.toLowerCase() })}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>

            {/* AI Assistant Promo */}
            <div className="card p-6 bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <h3 className="font-semibold text-purple-900">AI Assistant</h3>
              </div>
              <p className="text-sm text-purple-700 mb-4">
                Get personalized style advice, trend analysis, and fashion predictions powered by AI!
              </p>
              <button 
                onClick={openAIChat}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-lg font-medium hover:from-purple-600 hover:to-pink-600 transition-colors"
              >
                Chat with AI
              </button>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-3">
            {renderMainContent()}
          </div>
        </div>
      </main>

      {/* Floating AI Chat Button */}
      <button
        onClick={openAIChat}
        className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110 flex items-center justify-center z-40"
        aria-label="Open AI Chat"
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {/* AI Chat Modal */}
      <AIChat 
        isOpen={isChatOpen} 
        onClose={closeAIChat} 
        initialContext={chatContext}
        resetChat={resetChat}
      />

      {/* Comprehensive Analysis Modal */}
      {comprehensiveAnalysisTrend && (
        <ComprehensiveAnalysis
          trend={comprehensiveAnalysisTrend}
          onClose={closeComprehensiveAnalysis}
        />
      )}

      {/* Data Enrichment Modal */}
      <DataEnrichment
        isOpen={isDataEnrichmentOpen}
        onClose={() => setIsDataEnrichmentOpen(false)}
      />

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 mt-16 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="md:col-span-2">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-8 h-8 fashion-gradient rounded-lg flex items-center justify-center shadow-md">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <span className="text-lg font-bold text-gradient font-fashion">
                  Fashioning.ai
                </span>
              </div>
              <p className="text-gray-600 mb-4 leading-relaxed">
                Discover the latest fashion trends powered by AI. Get insights into emerging styles, 
                sustainable fashion, and global fashion movements with real-time data and predictive analytics.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">Features</h4>
              <ul className="space-y-2 text-gray-600">
                <li className="hover:text-primary-600 transition-colors cursor-pointer">Trend Discovery</li>
                <li className="hover:text-primary-600 transition-colors cursor-pointer">AI Analysis</li>
                <li className="hover:text-primary-600 transition-colors cursor-pointer">Global Insights</li>
                <li className="hover:text-primary-600 transition-colors cursor-pointer">Sustainability Score</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">Support</h4>
              <ul className="space-y-2 text-gray-600">
                <li className="hover:text-primary-600 transition-colors cursor-pointer">Help Center</li>
                <li className="hover:text-primary-600 transition-colors cursor-pointer">API Documentation</li>
                <li className="hover:text-primary-600 transition-colors cursor-pointer">Contact Us</li>
                <li className="hover:text-primary-600 transition-colors cursor-pointer">Privacy Policy</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-100 mt-8 pt-8 text-center text-gray-500">
            <p>&copy; 2025 Fashioning.ai. All rights reserved. | Built with AI for the future of fashion.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
