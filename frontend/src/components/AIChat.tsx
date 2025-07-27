import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Loader2, MessageCircle, X } from 'lucide-react';
import { fashionApi } from '../services/api';

interface ChatMessage {
  id: string;
  message: string;
  response?: string;
  type: 'user' | 'ai';
  timestamp: Date;
  aiType?: 'trend_analysis' | 'style_advice' | 'prediction' | 'general';
}

interface AIChatProps {
  isOpen: boolean;
  onClose: () => void;
  initialContext?: any;
  resetChat?: boolean;
}

const AIChat: React.FC<AIChatProps> = ({ isOpen, onClose, initialContext, resetChat }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    loadSuggestions();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Auto-send trend analysis when context is provided
  useEffect(() => {
    if (isOpen && initialContext && initialContext.trends && initialContext.trends.length > 0) {
      const trend = initialContext.trends[0];
      const autoMessage = `Tell me everything about this fashion trend: "${trend.name}". I want to know about its popularity, who's wearing it, and how I can style it.`;
      
      // Only auto-send if there are no messages yet (fresh chat)
      if (messages.length === 0) {
        setTimeout(() => {
          sendMessage(autoMessage);
        }, 500); // Small delay for better UX
      }
    }
  }, [isOpen, initialContext, messages.length]);

  // Reset chat when resetChat prop changes
  useEffect(() => {
    if (resetChat) {
      setMessages([]);
      setInputMessage('');
    }
  }, [resetChat]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadSuggestions = async () => {
    try {
      const response = await fashionApi.getAISuggestions();
      setSuggestions(response.data.suggestions);
    } catch (error) {
      console.error('Error loading suggestions:', error);
    }
  };

  const sendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      message: message.trim(),
      type: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fashionApi.chatWithAI({
        message: message.trim(),
        context: initialContext
      });

      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        message: response.data.response,
        type: 'ai',
        timestamp: new Date(),
        aiType: response.data.type,
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        message: "I'm having trouble responding right now. Please try again in a moment!",
        type: 'ai',
        timestamp: new Date(),
        aiType: 'general',
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputMessage);
  };

  const handleSuggestionClick = (suggestion: string) => {
    sendMessage(suggestion);
  };

  const getAITypeIcon = (type: string) => {
    switch (type) {
      case 'trend_analysis':
        return '📊';
      case 'style_advice':
        return '💅';
      case 'prediction':
        return '🔮';
      default:
        return '✨';
    }
  };

  const formatAIResponse = (response: string) => {
    // Convert markdown-like formatting to HTML
    return response
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/• /g, '&bull; ')
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0)
      .map((line, index) => (
        <div key={index} dangerouslySetInnerHTML={{ __html: line }} />
      ));
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl h-[600px] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">AI Fashion Assistant</h3>
              <p className="text-sm text-gray-600">Your personal style advisor</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageCircle className="w-8 h-8 text-purple-500" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Welcome to your AI Fashion Assistant!</h4>
              <p className="text-gray-600 mb-6">Ask me anything about fashion trends, style advice, or predictions.</p>
              
              {/* Suggestions */}
              <div className="space-y-2">
                <p className="text-sm text-gray-500 mb-3">Try asking:</p>
                <div className="grid grid-cols-1 gap-2">
                  {suggestions.slice(0, 4).map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors text-sm"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-4 rounded-2xl ${
                  message.type === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                {message.type === 'ai' && (
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-lg">{getAITypeIcon(message.aiType || 'general')}</span>
                    <span className="text-xs text-gray-500 uppercase tracking-wide">
                      {message.aiType?.replace('_', ' ') || 'AI Assistant'}
                    </span>
                  </div>
                )}
                
                <div className={`space-y-2 ${message.type === 'ai' ? 'text-sm' : ''}`}>
                  {message.type === 'ai' 
                    ? formatAIResponse(message.message)
                    : message.message
                  }
                </div>
                
                <div className={`text-xs mt-2 ${
                  message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}>
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 p-4 rounded-2xl">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin text-purple-500" />
                  <span className="text-sm text-gray-600">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-6 border-t border-gray-200">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask about fashion trends, style advice, or predictions..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || isLoading}
              className="px-6 py-3 bg-purple-500 text-white rounded-xl hover:bg-purple-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AIChat; 