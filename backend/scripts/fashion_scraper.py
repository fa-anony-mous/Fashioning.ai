"""
Multi-Site Fashion Trend Scraper
Scrapes fashion trends from multiple websites and uploads to Algolia.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
import re
from typing import List, Dict, Any
import sys
import os

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algoliasearch.search.client import SearchClientSync
from app.core.config import settings

class FashionTrendScraper:
    def __init__(self):
        """Initialize the scraper with Algolia client"""
        if not settings.ALGOLIA_APP_ID or not settings.ALGOLIA_ADMIN_API_KEY:
            print("❌ Algolia credentials not configured")
            self.client = None
            return
            
        self.client = SearchClientSync(
            settings.ALGOLIA_APP_ID,
            settings.ALGOLIA_ADMIN_API_KEY
        )
        self.index_name = "fashion_trends"
        
        # Add websites to scrape
        self.websites = [
            "https://www.vogue.com/fashion",
            "https://www.vogue.com/runway", 
            "https://www.vogue.com/fashion-shows"
            # Add more fashion websites here
        ]

        # Fashion categories mapping
        self.category_keywords = {
            "luxury": ["luxury", "couture", "haute", "premium", "exclusive", "designer", "high-end"],
            "streetwear": ["streetwear", "urban", "casual", "street", "sneakers", "hoodie", "oversized"],
            "sustainable": ["sustainable", "eco-friendly", "organic", "recycled", "ethical", "green"],
            "vintage": ["vintage", "retro", "classic", "heritage", "throwback", "nostalgic"],
            "minimalist": ["minimalist", "minimal", "clean", "simple", "understated", "essential"],
            "maximalist": ["maximalist", "bold", "dramatic", "statement", "extravagant", "ornate"],
            "athleisure": ["athleisure", "athletic", "sporty", "activewear", "performance", "gym"],
            "formal": ["formal", "business", "professional", "suit", "tailored", "corporate"],
            "casual": ["casual", "everyday", "comfortable", "relaxed", "easy", "laid-back"],
            "avant-garde": ["avant-garde", "experimental", "innovative", "cutting-edge", "artistic", "conceptual"]
        }

        # Region mapping based on fashion weeks and brands
        self.region_mapping = {
            "North America": ["new york", "nyfw", "lafw", "canada", "american", "us", "united states"],
            "Europe": ["paris", "pfw", "milan", "mfw", "london", "lfw", "european", "french", "italian", "british"],
            "Asia Pacific": ["tokyo", "tfw", "seoul", "sfw", "shanghai", "asian", "japanese", "korean", "chinese"],
            "Latin America": ["sao paulo", "spfw", "mexico", "brazil", "latin", "south american"],
            "Middle East": ["dubai", "abudhabi", "middle east", "arabic", "gulf"],
            "Africa": ["lagos", "africa", "african", "nigerian", "south african"]
        }

        # Headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def fetch_html(self, url):
        """Fetch HTML content from a URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
            return None

    def identify_category(self, text):
        """Identify fashion category based on text content"""
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        # Return the category with the highest score, or default to "casual"
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return "casual"

    def identify_regions(self, text):
        """Identify regions based on text content"""
        text_lower = text.lower()
        detected_regions = []
        
        for region, keywords in self.region_mapping.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_regions.append(region)
        
        # If no specific region detected, default to global
        if not detected_regions:
            detected_regions = ["Global"]
        
        return detected_regions

    def extract_images(self, soup):
        """Extract image URLs from HTML"""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and re.search(r'\.(jpg|jpeg|png|webp|gif)', src, re.IGNORECASE):
                # Convert relative URLs to absolute
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = 'https://www.vogue.com' + src
                images.append(src)
        return list(set(images))  # Remove duplicates

    def calculate_trend_score(self, social_mentions: int, influencer_count: int, brand_count: int) -> float:
        """Calculate a trend score based on various metrics"""
        # Normalize and weight different factors
        social_score = min(social_mentions / 10000, 1.0) * 0.4
        influencer_score = min(influencer_count / 100, 1.0) * 0.3
        brand_score = min(brand_count / 20, 1.0) * 0.3
        
        return round(social_score + influencer_score + brand_score, 2)

    def parse_fashion_articles(self, html, source_url):
        """Parse fashion articles from HTML content"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []

        # Look for article elements
        article_tags = soup.find_all(['article', 'div'], class_=re.compile(r'(article|story|show|collection|post)'))
        
        for article in article_tags[:15]:  # Limit to 15 articles per site
                try:
                    # Extract title
                title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
                if not title_elem:
                    continue
                        title = title_elem.get_text(strip=True)
                        
                        # Extract description
                desc_elem = article.find(['p', 'div'], class_=re.compile(r'(description|summary|excerpt)'))
                        description = desc_elem.get_text(strip=True) if desc_elem else ""
                        
                # Extract tags/keywords
                tag_elems = article.find_all(['span', 'a'], class_=re.compile(r'(tag|keyword|category)'))
                tags = [tag.get_text(strip=True) for tag in tag_elems if tag.get_text(strip=True)]
                
                # Extract brand/designer
                brand_elem = article.find(['span', 'a'], class_=re.compile(r'(brand|designer|label)'))
                brand = brand_elem.get_text(strip=True) if brand_elem else ""
                
                # Skip if no meaningful content
                if len(title) < 10:
                    continue
            
                # Combine text for analysis
                full_text = f"{title} {description} {' '.join(tags)} {brand}"
                
                # Categorize the trend
                category = self.identify_category(full_text)
                
                # Detect regions
                regions = self.identify_regions(full_text)
                
                # Extract images
                images = self.extract_images(article)
                
                # Generate trend data
                            trend = {
                    "objectID": f"fashion_{len(results) + 1}_{int(time.time())}",
                    "name": title,
                    "category": category,
                    "description": description or f"Latest trend from {brand}" if brand else "Fashion trend",
                    "regions": regions,
                    "brand": brand,
                    "source": source_url,
                    "source_url": source_url,
                    "image_url": images[0] if images else "",
                    "trend_score": self.calculate_trend_score(
                        social_mentions=len(tags) * 100,  # Estimate based on tags
                        influencer_count=len([t for t in tags if 'influencer' in t.lower()]),
                        brand_count=1 if brand else 0
                    ),
                    "growth_rate": round(10 + (len(tags) * 2), 1),  # Estimate growth
                    "color_palette": ["#000000", "#FFFFFF", "#808080"],  # Default palette
                    "demographics": {
                        "primary_age": "18-35",
                        "secondary_age": "36-50",
                        "gender_split": {"female": 70, "male": 30}
                    },
                    "sustainability_score": 0.5,  # Default score
                    "predicted_peak": (datetime.now() + timedelta(days=90)).isoformat(),
                    "social_mentions": len(tags) * 100,
                    "influencer_adoptions": len([t for t in tags if 'influencer' in t.lower()]),
                    "brand_adoptions": [brand] if brand else [],
                    "tags": tags,
                    "images": images,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "type": "trend"
                }
                
                results.append(trend)
                print(f"   ✅ Extracted: {title[:50]}... ({category})")
                            
                except Exception as e:
                print(f"   ⚠️ Error processing article: {str(e)}")
                    continue
        
        return results

    def scrape_all_sites(self):
        """Scrape all configured websites"""
        all_trends = []
        
        for website in self.websites:
            print(f"🔍 Scraping: {website}")
            html = self.fetch_html(website)
            if html:
                trends = self.parse_fashion_articles(html, website)
                all_trends.extend(trends)
                print(f"   📊 Found {len(trends)} trends from {website}")
            else:
                print(f"   ❌ Failed to fetch {website}")
        
        return all_trends

    def upload_to_algolia(self, trends: List[Dict[str, Any]]) -> bool:
        """Upload trends to Algolia index"""
        if not self.client or not trends:
            return False
        
        try:
            print(f"🚀 Uploading {len(trends)} trends to Algolia...")
            
            # Upload trends in batches
            batch_size = 10
            for i in range(0, len(trends), batch_size):
                batch = trends[i:i + batch_size]
                
                for trend in batch:
                    response = self.client.save_object(
                        index_name=self.index_name,
                        body=trend
                    )
                    print(f"   ✅ Uploaded: {trend['name'][:30]}...")
                
                # Small delay between batches
                time.sleep(1)
            
            print("🎉 Successfully uploaded all trends to Algolia!")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading to Algolia: {str(e)}")
            return False
    
    def run(self):
        """Main execution method"""
        print("🌟 Starting Multi-Site Fashion Trend Scraper")
        print("=" * 50)
        
        # Scrape trends from all sites
        trends = self.scrape_all_sites()
        
        if trends:
            # Upload to Algolia
            success = self.upload_to_algolia(trends)
            if success:
                print(f"\n🎯 Summary:")
                print(f"   - Trends scraped: {len(trends)}")
                print(f"   - Categories found: {set(t['category'] for t in trends)}")
                print(f"   - Regions covered: {set(region for t in trends for region in t['regions'])}")
                print(f"   - Sources: {set(t['source'] for t in trends)}")
                print(f"\n🔗 Test your API:")
                print(f"   - GET /api/v1/trends")
                print(f"   - GET /api/v1/trends?category=luxury")
                print(f"   - GET /api/v1/trends?region=North America")
                print(f"   - GET /api/v1/trends?category=streetwear&region=Europe")
            else:
                print("❌ Failed to upload trends to Algolia")
        else:
            print("❌ No trends found to upload")

def main():
    """Main function"""
    scraper = FashionTrendScraper()
    scraper.run()

if __name__ == "__main__":
    main()