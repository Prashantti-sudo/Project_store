import os
import base64
from typing import Dict, Any, Optional
import asyncio
import openai
from anthropic import Anthropic
import google.generativeai as genai


class LLMService:
    def __init__(self):
        self.provider = os.getenv("PRIMARY_LLM_PROVIDER", "openai").lower()
        
        # Initialize OpenAI (only if API key is provided)
        self.openai_client = None
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key.strip() and openai_key != "your_openai_api_key_here":
            try:
                openai.api_key = openai_key
                self.openai_client = openai.OpenAI(api_key=openai_key)
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {str(e)}")
        
        # Initialize Anthropic (only if API key is provided)
        self.anthropic_client = None
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key and anthropic_key.strip() and anthropic_key != "your_anthropic_api_key_here":
            try:
                self.anthropic_client = Anthropic(api_key=anthropic_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Anthropic client: {str(e)}")
        
        # Initialize Google Gemini (only if API key is provided)
        self.google_model = None
        self.google_vision_model = None
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key and google_key.strip() and google_key != "your_google_api_key_here":
            try:
                genai.configure(api_key=google_key)
                # Use gemini-pro for text and gemini-pro-vision for images (correct model names)
                self.google_model = genai.GenerativeModel('gemini-pro')
                self.google_vision_model = genai.GenerativeModel('gemini-pro-vision')
                print("Gemini API initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize Google Gemini: {str(e)}")
    
    async def analyze_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Analyze an image using LLM to extract category, description, and keywords.
        """
        try:
            # Encode image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            prompt = """Analyze this product image and classify it into ONE of these categories based on visual style:
- "Artist" - Hand-drawn, artistic, creative illustrations
- "Cartoonist" - Cartoon-style, animated, playful illustrations
- "Sticker" - Sticker-style, simple, bold graphics
- "Realistic Image Store" - Photorealistic, professional product photography

Also provide:
1. A brief description (2-3 sentences)
2. 5-10 relevant keywords for advertising

Format your response as JSON with keys: description, category (must be one of the 4 above), keywords (array), category_description.
Be concise and marketing-focused."""
            
            if self.provider == "openai" and hasattr(self, 'openai_client'):
                return await self._analyze_with_openai(image_data, prompt)
            elif self.provider == "anthropic" and hasattr(self, 'anthropic_client'):
                return await self._analyze_with_anthropic(image_base64, prompt)
            elif self.provider == "google" and hasattr(self, 'google_model'):
                return await self._analyze_with_google(image_data, prompt)
            else:
                # Fallback to default analysis
                return self._default_image_analysis()
        
        except Exception as e:
            print(f"Error in LLM image analysis: {str(e)}")
            return self._default_image_analysis()
    
    async def _analyze_with_openai(self, image_data: bytes, prompt: str) -> Dict[str, Any]:
        """Analyze image using OpenAI GPT-4 Vision"""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.openai_client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=300
                )
            )
            
            result_text = response.choices[0].message.content
            return self._parse_llm_response(result_text)
        except Exception as e:
            print(f"OpenAI analysis error: {str(e)}")
            return self._default_image_analysis()
    
    async def _analyze_with_anthropic(self, image_base64: str, prompt: str) -> Dict[str, Any]:
        """Analyze image using Anthropic Claude"""
        try:
            loop = asyncio.get_event_loop()
            message = await loop.run_in_executor(
                None,
                lambda: self.anthropic_client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=300,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/jpeg",
                                        "data": image_base64
                                    }
                                },
                                {"type": "text", "text": prompt}
                            ]
                        }
                    ]
                )
            )
            
            result_text = message.content[0].text
            return self._parse_llm_response(result_text)
        except Exception as e:
            print(f"Anthropic analysis error: {str(e)}")
            return self._default_image_analysis()
    
    async def _analyze_with_google(self, image_data: bytes, prompt: str) -> Dict[str, Any]:
        """Analyze image using Google Gemini Vision"""
        try:
            import PIL.Image
            import io
            
            if not hasattr(self, 'google_vision_model') or self.google_vision_model is None:
                if not hasattr(self, 'google_model') or self.google_model is None:
                    return self._default_image_analysis()
                # Fallback to text model if vision model not available
                model = self.google_model
            else:
                model = self.google_vision_model
            
            image = PIL.Image.open(io.BytesIO(image_data))
            loop = asyncio.get_event_loop()
            
            response = await loop.run_in_executor(
                None,
                lambda: model.generate_content([prompt, image])
            )
            
            result_text = response.text
            return self._parse_llm_response(result_text)
        except Exception as e:
            print(f"Google Gemini analysis error: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._default_image_analysis()
    
    async def analyze_product(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze product information and generate marketing insights.
        Note: Image analysis for category is done separately in main.py
        """
        try:
            product_text = f"""
Product Title: {product_info.get('title', 'N/A')}
Description: {product_info.get('description', 'N/A')}
Price: {product_info.get('price', 'N/A')}

Analyze this product and provide:
1. 10-15 bold, eye-catching marketing keywords (for ad text overlays) - make them SHORT and POWERFUL
2. 3-5 suggested ad captions (short, compelling, high-converting)
3. A primary call-to-action keyword (single word or short phrase like "SHOP NOW", "BUY NOW", "GET IT")
4. Target audience insights

Format as JSON with keys: keywords (array), captions (array), primary_cta, target_audience.
Focus on high-converting, bold keywords that work well in ad creatives. Keywords should be UPPERCASE and attention-grabbing.
"""
            
            loop = asyncio.get_event_loop()
            
            if self.provider == "openai" and hasattr(self, 'openai_client'):
                response = await loop.run_in_executor(
                    None,
                    lambda: self.openai_client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": product_text}],
                        max_tokens=400
                    )
                )
                result_text = response.choices[0].message.content
            elif self.provider == "anthropic" and hasattr(self, 'anthropic_client'):
                message = await loop.run_in_executor(
                    None,
                    lambda: self.anthropic_client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=400,
                        messages=[{"role": "user", "content": product_text}]
                    )
                )
                result_text = message.content[0].text
            elif self.provider == "google" and hasattr(self, 'google_model'):
                response = await loop.run_in_executor(
                    None,
                    lambda: self.google_model.generate_content(product_text)
                )
                result_text = response.text
            else:
                return self._default_product_analysis(product_info)
            
            return self._parse_llm_response(result_text)
        
        except Exception as e:
            print(f"Error in LLM product analysis: {str(e)}")
            return self._default_product_analysis(product_info)
    
    def _parse_llm_response(self, text: str) -> Dict[str, Any]:
        """Parse LLM response text into structured format"""
        import json
        import re
        
        # Try to extract JSON from response
        json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        # Fallback parsing
        result = {
            "description": text[:200] if text else "AI-generated description",
            "category": "General",
            "keywords": self._extract_keywords(text),
            "captions": []
        }
        
        return result
    
    def _extract_keywords(self, text: str) -> list:
        """Extract potential keywords from text"""
        import re
        # Simple keyword extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        # Remove common words
        stop_words = {'this', 'that', 'with', 'from', 'have', 'will', 'would', 'could', 'should'}
        keywords = [w for w in set(words) if w not in stop_words][:10]
        return keywords[:10]
    
    def _default_image_analysis(self) -> Dict[str, Any]:
        """Default analysis when LLM fails"""
        return {
            "description": "High-quality image ready for motion effects",
            "category": "Realistic Image Store",
            "category_description": "Standard product image",
            "keywords": ["premium", "quality", "professional", "modern", "creative"]
        }
    
    def _default_product_analysis(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """Default analysis when LLM fails"""
        title = product_info.get('title', 'Product')
        return {
            "keywords": ["PREMIUM", "QUALITY", "EXCLUSIVE", "LIMITED", "NOW"] + title.upper().split()[:5],
            "captions": [
                f"Discover {title}",
                f"Premium {title}",
                f"Get {title} Now"
            ],
            "primary_cta": "Shop Now",
            "target_audience": "General consumers"
        }

