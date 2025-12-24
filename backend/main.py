from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
import os
from dotenv import load_dotenv

from services.llm_service import LLMService
from services.image_service import ImageService
from services.motion_service import MotionService
from services.product_scraper import ProductScraper

load_dotenv()

app = FastAPI(
    title="AI Ad Creative Generator API",
    description="Premium AI-powered ad creative generation platform",
    version="1.0.0"
)

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
llm_service = LLMService()
image_service = ImageService()
motion_service = MotionService()
product_scraper = ProductScraper()


class ProductURLRequest(BaseModel):
    product_url: HttpUrl


@app.get("/")
async def root():
    return {
        "message": "AI Ad Creative Generator API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/generate-motion-effect")
async def generate_motion_effect(image: UploadFile = File(...)):
    """
    Generate motion effects from an uploaded image.
    """
    try:
        # Validate file type
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await image.read()
        
        # Analyze image with LLM
        analysis = await llm_service.analyze_image(image_data)
        
        # Generate motion effect
        motion_result = await motion_service.generate_motion_effect(
            image_data=image_data,
            analysis=analysis
        )
        
        return {
            "status": "success",
            "motion_effect_url": motion_result.get("url"),
            "analysis": analysis.get("description"),
            "category": analysis.get("category"),
            "keywords": analysis.get("keywords", []),
            "download_url": motion_result.get("download_url")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating motion effect: {str(e)}")


@app.post("/api/generate-ad-from-url")
async def generate_ad_from_url(request: ProductURLRequest):
    """
    Generate ad creatives from a product URL with category classification and multiple sizes.
    """
    try:
        # Scrape product information
        product_info = await product_scraper.scrape_product(request.product_url)
        
        if not product_info:
            raise HTTPException(status_code=400, detail="Could not extract product information from URL")
        
        # Fetch and analyze product image for category classification
        category = "Realistic Image Store"
        category_description = "Standard product image"
        
        if product_info.get("image_url"):
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(product_info["image_url"]) as img_response:
                        if img_response.status == 200:
                            image_data = await img_response.read()
                            image_analysis = await llm_service.analyze_image(image_data)
                            category = image_analysis.get("category", "Realistic Image Store")
                            category_description = image_analysis.get("category_description", "AI-analyzed visual style")
            except Exception as e:
                print(f"Error analyzing product image: {str(e)}")
        
        # Analyze product with LLM for keywords and captions
        analysis = await llm_service.analyze_product(product_info)
        
        # Generate ad creatives in multiple sizes
        ad_creatives = await image_service.generate_ad_creatives(
            product_info=product_info,
            analysis=analysis,
            category=category
        )
        
        # Debug: Log ad_sizes structure
        print(f"Generated ad_sizes: {list(ad_creatives.get('ad_sizes', {}).keys())}")
        for platform, ad_data in ad_creatives.get('ad_sizes', {}).items():
            if ad_data and 'url' in ad_data:
                url_preview = ad_data['url'][:100] if len(ad_data['url']) > 100 else ad_data['url']
                print(f"  {platform}: URL length={len(ad_data['url'])}, preview={url_preview}...")
        
        return {
            "status": "success",
            "category": category,
            "category_description": category_description,
            "product_info": {
                "title": product_info.get("title"),
                "description": product_info.get("description"),
                "price": product_info.get("price"),
                "image_url": product_info.get("image_url")
            },
            "ad_sizes": ad_creatives.get("ad_sizes", {}),
            "ad_images": ad_creatives.get("images", []),
            "keywords": analysis.get("keywords", []),
            "suggested_captions": analysis.get("captions", []),
            "primary_cta": analysis.get("primary_cta", "Shop Now")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ad creative: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )

