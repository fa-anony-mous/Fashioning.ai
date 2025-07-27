"""
Gemini AI Service for Fashion Recommendations
Integrates with Google's Gemini API to provide intelligent fashion insights
"""

import os
import json
from typing import Dict, List, Any, Optional
from app.core.config import settings
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for integrating with Google Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini service"""
        self.api_key = settings.GEMINI_API_KEY
        self.is_configured = bool(self.api_key)
        
        if self.is_configured:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
                logger.info("Gemini 2.0 flash exp configured successfully")
            except Exception as e:
                logger.error(f"Failed to configure Gemini: {e}")
                self.is_configured = False
        else:
            logger.warning("Gemini API key not configured. Using mock responses.")
    
    async def analyze_trend(self, trend_data: Dict[str, Any]) -> str:
        """
        Analyze a specific fashion trend using Gemini AI
        """
        if not self.is_configured:
            return self._generate_mock_trend_analysis(trend_data)
        
        try:
            prompt = f"""
            Analyze this fashion trend and provide detailed insights:
            
            Trend Name: {trend_data.get('name', 'Unknown')}
            Category: {trend_data.get('category', 'Unknown')}
            Description: {trend_data.get('description', 'No description')}
            Trend Score: {trend_data.get('trend_score', 0)}
            Growth Rate: {trend_data.get('growth_rate', 0)}%
            Target Demographics: {trend_data.get('demographics', {})}
            Regions: {', '.join(trend_data.get('regions', []))}
            Color Palette: {trend_data.get('color_palette', [])}
            Sustainability Score: {trend_data.get('sustainability_score', 0)}
            Brand Adoptions: {trend_data.get('brand_adoptions', [])}
            Tags: {trend_data.get('tags', [])}
            
            Please provide a comprehensive analysis including:
            1. Key insights about this trend's popularity and appeal
            2. Why it's gaining traction and who's driving it
            3. Target audience and demographics
            4. How to style and incorporate this trend
            5. Shopping recommendations and brand suggestions
            6. Future outlook and sustainability considerations
            
            Make your response engaging, specific to this trend, and actionable for fashion enthusiasts.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error analyzing trend with Gemini: {e}")
            return self._generate_mock_trend_analysis(trend_data)
    
    async def get_style_recommendations(self, user_preferences: Dict[str, Any], trends: List[Dict[str, Any]]) -> str:
        """
        Get personalized style recommendations based on user preferences and current trends
        """
        if not self.is_configured:
            return self._generate_mock_style_recommendations(user_preferences, trends)
        
        try:
            preferences_text = self._format_preferences(user_preferences)
            trends_text = self._format_trends(trends[:5])  # Top 5 trends
            
            prompt = f"""
            As a fashion AI assistant, provide personalized style recommendations:
            
            User Preferences:
            {preferences_text}
            
            Current Trending Items:
            {trends_text}
            
            Please provide:
            1. 3-5 specific style recommendations tailored to the user's preferences
            2. How to incorporate current trends into their personal style
            3. Shopping suggestions with specific brands and pieces
            4. Practical styling tips and outfit combinations
            5. Seasonal considerations and versatility advice
            
            Make your response personal, actionable, and specific to the user's style preferences.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error getting style recommendations: {e}")
            return self._generate_mock_style_recommendations(user_preferences, trends)
    
    async def predict_future_trends(self, current_trends: List[Dict[str, Any]]) -> str:
        """
        Predict future fashion trends based on current data
        """
        if not self.is_configured:
            return self._generate_mock_trend_predictions(current_trends)
        
        try:
            trends_summary = self._summarize_trends(current_trends)
            
            prompt = f"""
            Based on these current fashion trends, predict what's coming next:
            
            Current Trends Analysis:
            {trends_summary}
            
            Please provide:
            1. 3-5 emerging trends you predict will gain popularity
            2. The reasoning behind each prediction
            3. Timeline estimates for when these trends will peak
            4. How these trends will evolve from current ones
            5. Recommendations for early adoption strategies
            
            Make your predictions data-driven and specific to the fashion industry.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error predicting trends: {e}")
            return self._generate_mock_trend_predictions(current_trends)
    
    async def chat_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Generate a conversational response to user messages
        """
        if not self.is_configured:
            return self._generate_general_response(message, context)
        
        try:
            # Check if we have specific trend data from a clicked card
            trend_data = context.get('trend_data') if context else None
            
            if trend_data and "trend" in message.lower():
                # User is asking about a specific trend - provide detailed analysis
                prompt = f"""
                The user is asking about this specific fashion trend: "{trend_data.get('name', 'Unknown')}"
                
                Trend Details:
                - Name: {trend_data.get('name', 'Unknown')}
                - Category: {trend_data.get('category', 'Unknown')}
                - Description: {trend_data.get('description', 'No description')}
                - Trend Score: {trend_data.get('trend_score', 0)}
                - Growth Rate: {trend_data.get('growth_rate', 0)}%
                - Color Palette: {trend_data.get('color_palette', [])}
                - Sustainability Score: {trend_data.get('sustainability_score', 0)}
                - Brand Adoptions: {trend_data.get('brand_adoptions', [])}
                - Regions: {', '.join(trend_data.get('regions', []))}
                - Target Demographics: {trend_data.get('demographics', {})}
                
                User Question: "{message}"
                
                Please provide a comprehensive, engaging response that:
                1. Directly addresses the user's specific question about this trend
                2. Uses the actual trend data provided (colors, brands, demographics, etc.)
                3. Gives specific styling advice based on the trend's characteristics
                4. Mentions the actual sustainability score and what it means
                5. Suggests specific brands from the brand_adoptions list
                6. Explains who's wearing this trend based on the demographics
                7. Provides actionable styling tips using the color palette
                
                Make your response personal, specific to this exact trend, and actionable.
                """
                
                response = self.model.generate_content(prompt)
                return response.text
            
            # Analyze user intent for general queries
            intent = self._analyze_intent(message)
            
            if intent == "trend_analysis" and context and context.get('trends'):
                # Use the first trend from the trends list
                trend = context['trends'][0]
                return await self.analyze_trend(trend)
            elif intent == "style_advice":
                trends = context.get('trends', []) if context else []
                return await self.get_style_recommendations({}, trends)
            elif intent == "trend_prediction":
                trends = context.get('trends', []) if context else []
                return await self.predict_future_trends(trends)
            else:
                # General conversation
                prompt = f"""
                You are a helpful fashion AI assistant. The user said: "{message}"
                
                Context: {context or 'No specific context provided'}
                
                Please provide a helpful, engaging response about fashion trends, style advice, or general fashion questions.
                Be conversational, knowledgeable, and specific to their query.
                """
                
                response = self.model.generate_content(prompt)
                return response.text
                
        except Exception as e:
            logger.error(f"Error in chat response: {e}")
            return self._generate_general_response(message, context)
    
    def _generate_mock_trend_analysis(self, trend_data: Dict[str, Any]) -> str:
        """Generate intelligent trend analysis based on data"""
        name = trend_data.get('name', 'This trend')
        category = trend_data.get('category', 'fashion')
        growth_rate = trend_data.get('growth_rate', 0)
        sustainability_score = trend_data.get('sustainability_score', 0)
        color_palette = trend_data.get('color_palette', [])
        regions = trend_data.get('regions', ['Global'])
        
        return f"""
        💅 **{name}** - Trend Analysis
        
        📊 **Key Insights:**
        • This {category} trend is showing a {growth_rate}% growth rate
        • Popular in {', '.join(regions)} markets
        • Sustainability score: {sustainability_score * 100:.0f}%
        
        🎨 **Color Palette:** {', '.join(color_palette) if color_palette else 'Not specified'}
        
        👥 **Target Audience:** Fashion enthusiasts looking for {category} styles
        
        💡 **Styling Tips:**
        • Incorporate this trend gradually into your existing wardrobe
        • Focus on versatile pieces that can be styled multiple ways
        • Consider sustainable alternatives when possible
        
        🛍️ **Shopping Strategy:**
        • Start with one statement piece
        • Build around your existing favorites
        • Look for quality over quantity
        """
    
    def _generate_mock_style_recommendations(self, preferences: Dict[str, Any], trends: List[Dict[str, Any]]) -> str:
        """Generate personalized style recommendations"""
        if not trends:
            return "I'd be happy to provide style recommendations! Could you tell me more about your style preferences and what you're looking for?"
        
        trend = trends[0] if trends else {}
        name = trend.get('name', 'current trends')
        category = trend.get('category', 'fashion')
        
        return f"""
        💅 **Personalized Style Recommendations**
        
        ✨ **Top Pick:** Embrace the {name} aesthetic
        • Perfect for {category} enthusiasts
        • Trending in {', '.join(trend.get('regions', ['Global']))}
        • Consider sustainable alternatives when possible
        
        👗 **How to Style:**
        • Incorporate {', '.join(trend.get('color_palette', ['#000000', '#FFFFFF', '#808080']))} into your color scheme
        • Build versatile, comfortable outfits
        • Focus on versatile pieces
        
        🛍️ **Shopping Strategy:**
        • Look for pieces from {', '.join(trend.get('brand_adoptions', ['icon']))}
        • Start with one statement piece
        • Build around your existing favorites
        
        💡 **Pro Tip:** This trend has a {trend.get('sustainability_score', 0.5) * 100:.0f}% sustainability score - consider sustainable alternatives when possible
        """
    
    def _generate_mock_trend_predictions(self, trends: List[Dict[str, Any]]) -> str:
        """Generate future trend predictions"""
        if not trends:
            return "Based on current fashion patterns, I predict continued growth in sustainable fashion, tech-integrated clothing, and personalized style experiences."
        
        return f"""
        🔮 **Future Trend Predictions**
        
        Based on analyzing {len(trends)} current trends, here's what I predict:
        
        📈 **Emerging Trends:**
        1. **Sustainable Luxury** - Continued growth in eco-conscious premium fashion
        2. **Tech-Integrated Style** - Smart fabrics and wearable technology
        3. **Personalized Fashion** - AI-driven customization and recommendations
        
        ⏰ **Timeline:** Expect these trends to peak in the next 6-12 months
        
        💡 **Early Adoption Strategy:**
        • Start with sustainable materials in your purchases
        • Explore tech-enhanced accessories
        • Focus on versatile, timeless pieces
        """
    
    def _analyze_intent(self, message: str) -> str:
        """Analyze user message to determine intent"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["analyze", "analysis", "insights", "about this trend"]):
            return "trend_analysis"
        elif any(word in message_lower for word in ["recommend", "style", "what should i wear", "outfit"]):
            return "style_advice"
        elif any(word in message_lower for word in ["predict", "future", "next", "coming", "will be"]):
            return "trend_prediction"
        else:
            return "general"
    
    def _generate_general_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """Generate general fashion-related response"""
        return f"""
        👋 Hello! I'm your AI fashion assistant. I can help you with:
        
        📊 **Trend Analysis** - Get insights on current fashion trends
        💅 **Style Advice** - Personalized recommendations based on your preferences  
        🔮 **Future Predictions** - What's coming next in fashion
        🛍️ **Shopping Guidance** - Where and what to buy
        
        What would you like to explore today?
        """
    
    def _format_preferences(self, preferences: Dict[str, Any]) -> str:
        """Format user preferences for AI prompt"""
        if not preferences:
            return "No specific preferences provided"
        
        formatted = []
        if preferences.get("preferred_categories"):
            formatted.append(f"Categories: {', '.join(preferences['preferred_categories'])}")
        if preferences.get("preferred_regions"):
            formatted.append(f"Regions: {', '.join(preferences['preferred_regions'])}")
        if preferences.get("style_preferences"):
            formatted.append(f"Style: {', '.join(preferences['style_preferences'])}")
        
        return "\n".join(formatted) if formatted else "General fashion interest"
    
    def _format_trends(self, trends: List[Dict[str, Any]]) -> str:
        """Format trends data for AI prompt"""
        if not trends:
            return "No current trends available"
        
        formatted = []
        for trend in trends:
            formatted.append(f"• {trend.get('name', 'Unknown')} ({trend.get('category', 'general')}) - Score: {trend.get('trend_score', 0):.2f}")
        
        return "\n".join(formatted)
    
    def _summarize_trends(self, trends: List[Dict[str, Any]]) -> str:
        """Summarize trends for prediction analysis"""
        if not trends:
            return "No trends to analyze"
        
        categories = {}
        total_growth = 0
        
        for trend in trends:
            cat = trend.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            total_growth += trend.get('growth_rate', 0)
        
        avg_growth = total_growth / len(trends) if trends else 0
        top_category = max(categories.items(), key=lambda x: x[1])[0] if categories else "fashion"
        
        return f"""
        Total trends analyzed: {len(trends)}
        Average growth rate: {avg_growth:.1f}%
        Dominant category: {top_category}
        Top trending: {trends[0].get('name', 'Unknown') if trends else 'None'}
        """

# Create global instance
gemini_service = GeminiService() 