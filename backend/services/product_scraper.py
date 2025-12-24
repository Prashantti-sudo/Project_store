import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import re
import asyncio
import aiohttp


class ProductScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def scrape_product(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape product information from a URL.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(url), headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    response.raise_for_status()
                    content = await response.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Try to extract product information using common patterns
            product_info = {
                "title": self._extract_title(soup),
                "description": self._extract_description(soup),
                "price": self._extract_price(soup),
                "image_url": self._extract_image(soup),
                "category": self._extract_category(soup)
            }
            
            # Validate that we got at least a title
            if not product_info.get("title"):
                return None
            
            return product_info
        
        except Exception as e:
            print(f"Error scraping product: {str(e)}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract product title"""
        # Try multiple selectors
        selectors = [
            'h1.product-title',
            'h1[class*="title"]',
            'h1[class*="name"]',
            'meta[property="og:title"]',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '').strip()
                return element.get_text().strip()
        
        # Fallback: use page title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        return "Product"
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract product description"""
        selectors = [
            'meta[name="description"]',
            'meta[property="og:description"]',
            '.product-description',
            '[class*="description"]',
            'p[class*="description"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '').strip()
                text = element.get_text().strip()
                if text and len(text) > 20:
                    return text[:500]  # Limit length
        
        return ""
    
    def _extract_price(self, soup: BeautifulSoup) -> str:
        """Extract product price"""
        # Try to find price patterns
        price_patterns = [
            r'\$[\d,]+\.?\d*',
            r'€[\d,]+\.?\d*',
            r'£[\d,]+\.?\d*',
            r'[\d,]+\.?\d*\s*(USD|EUR|GBP)'
        ]
        
        text = soup.get_text()
        for pattern in price_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        
        # Try meta tags
        price_selectors = [
            'meta[property="product:price:amount"]',
            '[class*="price"]',
            '[id*="price"]'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    price = element.get('content', '')
                    if price:
                        return f"${price}"
                text = element.get_text().strip()
                if text:
                    return text
        
        return "Price not available"
    
    def _extract_image(self, soup: BeautifulSoup) -> str:
        """Extract product image URL"""
        selectors = [
            'meta[property="og:image"]',
            'img[class*="product"]',
            'img[class*="main"]',
            'img[alt*="product"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '')
                src = element.get('src') or element.get('data-src')
                if src:
                    return src
        
        return ""
    
    def _extract_category(self, soup: BeautifulSoup) -> str:
        """Extract product category"""
        selectors = [
            'meta[property="product:category"]',
            '[class*="category"]',
            '[class*="breadcrumb"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '')
                text = element.get_text().strip()
                if text:
                    return text.split('>')[-1].strip() if '>' in text else text
        
        return "General"

