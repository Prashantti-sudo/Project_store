import os
from typing import Dict, Any, List
import base64
from io import BytesIO
from PIL import Image


class ImageService:
    def __init__(self):
        self.api_key = os.getenv("IMAGE_GENERATION_API_KEY")
        self.provider = os.getenv("IMAGE_GENERATION_PROVIDER", "stability").lower()
    
    async def generate_ad_creatives(
        self,
        product_info: Dict[str, Any],
        analysis: Dict[str, Any],
        category: str = "Realistic Image Store"
    ) -> Dict[str, Any]:
        """
        Generate ad creative images from product information in multiple platform sizes.
        """
        try:
            # Get keywords and primary CTA
            keywords = analysis.get("keywords", [])[:5]  # Top 5 keywords
            primary_cta = analysis.get("primary_cta", "Shop Now")
            title = product_info.get("title", "Product")
            
            # Generate ad images in different sizes
            ad_sizes = {}
            
            # Facebook Feed - 1:1 (1080x1080)
            try:
                facebook_ad = await self._generate_ad_with_text(
                    product_info=product_info,
                    keywords=keywords,
                    primary_cta=primary_cta,
                    size=(1080, 1080),
                    category=category
                )
                if facebook_ad and facebook_ad.startswith('data:image'):
                    ad_sizes["facebook"] = {"url": facebook_ad, "size": "1080×1080", "ratio": "1:1"}
                else:
                    print(f"Warning: Facebook ad generation failed, using placeholder")
                    ad_sizes["facebook"] = {"url": self._create_placeholder_image(product_info, 0), "size": "1080×1080", "ratio": "1:1"}
            except Exception as e:
                print(f"Error generating Facebook ad: {str(e)}")
                ad_sizes["facebook"] = {"url": self._create_placeholder_image(product_info, 0), "size": "1080×1080", "ratio": "1:1"}
            
            # X/Twitter - 16:9 (1200x675)
            try:
                twitter_ad = await self._generate_ad_with_text(
                    product_info=product_info,
                    keywords=keywords,
                    primary_cta=primary_cta,
                    size=(1200, 675),
                    category=category
                )
                if twitter_ad and twitter_ad.startswith('data:image'):
                    ad_sizes["twitter"] = {"url": twitter_ad, "size": "1200×675", "ratio": "16:9"}
                else:
                    print(f"Warning: Twitter ad generation failed, using placeholder")
                    ad_sizes["twitter"] = {"url": self._create_placeholder_image(product_info, 0), "size": "1200×675", "ratio": "16:9"}
            except Exception as e:
                print(f"Error generating Twitter ad: {str(e)}")
                ad_sizes["twitter"] = {"url": self._create_placeholder_image(product_info, 0), "size": "1200×675", "ratio": "16:9"}
            
            # TikTok/Reels - 9:16 (1080x1920)
            try:
                tiktok_ad = await self._generate_ad_with_text(
                    product_info=product_info,
                    keywords=keywords,
                    primary_cta=primary_cta,
                    size=(1080, 1920),
                    category=category
                )
                if tiktok_ad and tiktok_ad.startswith('data:image'):
                    ad_sizes["tiktok"] = {"url": tiktok_ad, "size": "1080×1920", "ratio": "9:16"}
                else:
                    print(f"Warning: TikTok ad generation failed, using placeholder")
                    ad_sizes["tiktok"] = {"url": self._create_placeholder_image(product_info, 0), "size": "1080×1920", "ratio": "9:16"}
            except Exception as e:
                print(f"Error generating TikTok ad: {str(e)}")
                ad_sizes["tiktok"] = {"url": self._create_placeholder_image(product_info, 0), "size": "1080×1920", "ratio": "9:16"}
            
            return {
                "ad_sizes": ad_sizes,
                "images": [],  # Keep for backward compatibility
                "download_url": None
            }
        
        except Exception as e:
            print(f"Error generating ad creatives: {str(e)}")
            # Return placeholder images
            placeholder = self._create_placeholder_image(product_info, 0)
            return {
                "ad_sizes": {
                    "facebook": {"url": placeholder, "size": "1080×1080", "ratio": "1:1"},
                    "twitter": {"url": placeholder, "size": "1200×675", "ratio": "16:9"},
                    "tiktok": {"url": placeholder, "size": "1080×1920", "ratio": "9:16"}
                },
                "images": [],
                "download_url": None
            }
    
    async def _generate_ad_with_text(
        self,
        product_info: Dict[str, Any],
        keywords: List[str],
        primary_cta: str,
        size: tuple,
        category: str
    ) -> str:
        """Generate ad image with text overlays for specific size"""
        try:
            # Create base image or fetch product image
            product_image_url = product_info.get("image_url", "")
            title = product_info.get("title", "Product")
            
            # Create ad image with text overlay
            ad_image = await self._create_ad_image_with_overlay(
                product_image_url=product_image_url,
                title=title,
                keywords=keywords,
                primary_cta=primary_cta,
                size=size,
                category=category
            )
            
            return ad_image
        
        except Exception as e:
            print(f"Error generating ad with text: {str(e)}")
            return self._create_placeholder_image(product_info, 0)
    
    async def _create_ad_image_with_overlay(
        self,
        product_image_url: str,
        title: str,
        keywords: List[str],
        primary_cta: str,
        size: tuple,
        category: str
    ) -> str:
        """Create ad image with text overlays using PIL"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import aiohttp
            
            width, height = size
            
            # Create base image
            if product_image_url:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(product_image_url) as response:
                            if response.status == 200:
                                image_data = await response.read()
                                base_img = Image.open(BytesIO(image_data))
                                # Resize and crop to fit
                                base_img = self._resize_and_crop(base_img, (width, height))
                            else:
                                base_img = self._create_gradient_background(width, height, category)
                except:
                    base_img = self._create_gradient_background(width, height, category)
            else:
                base_img = self._create_gradient_background(width, height, category)
            
            # Create overlay for text
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Try to load a font, fallback to default
            try:
                # Try to use a bold font
                font_large = ImageFont.truetype("arial.ttf", size=int(height * 0.08))
                font_medium = ImageFont.truetype("arial.ttf", size=int(height * 0.05))
                font_small = ImageFont.truetype("arial.ttf", size=int(height * 0.04))
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Add semi-transparent background for text readability
            text_bg_height = int(height * 0.3)
            text_bg = Image.new('RGBA', (width, text_bg_height), (0, 0, 0, 180))
            overlay.paste(text_bg, (0, height - text_bg_height), text_bg)
            
            # Add title (truncate if too long)
            title_display = str(title)[:50] if len(str(title)) > 50 else str(title)
            title_y = height - text_bg_height + int(height * 0.05)
            try:
                # Get text bounding box for centering
                bbox = draw.textbbox((0, 0), title_display, font=font_large)
                text_width = bbox[2] - bbox[0]
                text_x = (width - text_width) // 2
                draw.text((text_x, title_y), title_display, fill=(255, 255, 255, 255), font=font_large)
            except Exception as e:
                print(f"Error drawing title: {str(e)}")
                # Fallback without font
                try:
                    draw.text((width // 2, title_y), title_display, fill=(255, 255, 255, 255))
                except:
                    pass
            
            # Add primary keyword/CTA
            if keywords and len(keywords) > 0:
                keyword_text = str(keywords[0]).upper()[:20]  # Limit length
                keyword_y = title_y + int(height * 0.08)
                try:
                    bbox = draw.textbbox((0, 0), keyword_text, font=font_medium)
                    text_width = bbox[2] - bbox[0]
                    text_x = (width - text_width) // 2
                    draw.text((text_x, keyword_y), keyword_text, fill=(255, 255, 0, 255), font=font_medium)
                except Exception as e:
                    print(f"Error drawing keyword: {str(e)}")
                    try:
                        draw.text((width // 2, keyword_y), keyword_text, fill=(255, 255, 0, 255))
                    except:
                        pass
            
            # Add CTA button
            cta_text = str(primary_cta).upper()[:15]  # Limit length
            cta_y = height - int(height * 0.08)
            cta_width = int(width * 0.4)
            cta_x = width // 2
            
            # Draw CTA background
            try:
                cta_bg = Image.new('RGBA', (cta_width, int(height * 0.1)), (255, 100, 0, 255))
                overlay.paste(cta_bg, (cta_x - cta_width // 2, cta_y - int(height * 0.05)), cta_bg)
                bbox = draw.textbbox((0, 0), cta_text, font=font_medium)
                text_width = bbox[2] - bbox[0]
                text_x = cta_x - text_width // 2
                draw.text((text_x, cta_y), cta_text, fill=(255, 255, 255, 255), font=font_medium)
            except Exception as e:
                print(f"Error drawing CTA: {str(e)}")
                try:
                    cta_bg = Image.new('RGBA', (cta_width, int(height * 0.1)), (255, 100, 0, 255))
                    overlay.paste(cta_bg, (cta_x - cta_width // 2, cta_y - int(height * 0.05)), cta_bg)
                    draw.text((cta_x, cta_y), cta_text, fill=(255, 255, 255, 255))
                except:
                    pass
            
            # Composite overlay on base image
            final_img = Image.alpha_composite(base_img.convert('RGBA'), overlay)
            final_img = final_img.convert('RGB')
            
            # Convert to base64 data URL
            try:
                output = BytesIO()
                final_img.save(output, format='PNG', quality=95, optimize=True)
                output.seek(0)
                
                import base64
                img_base64 = base64.b64encode(output.read()).decode('utf-8')
                data_url = f"data:image/png;base64,{img_base64}"
                
                # Verify the data URL is valid
                if len(img_base64) > 0:
                    print(f"Successfully generated image: {len(img_base64)} bytes")
                    return data_url
                else:
                    print("Error: Generated empty base64 image")
                    return self._create_placeholder_image({"title": title}, 0)
            except Exception as e:
                print(f"Error converting image to base64: {str(e)}")
                import traceback
                traceback.print_exc()
                return self._create_placeholder_image({"title": title}, 0)
        
        except Exception as e:
            print(f"Error creating ad image with overlay: {str(e)}")
            return self._create_placeholder_image({"title": title}, 0)
    
    def _resize_and_crop(self, img: Image.Image, size: tuple) -> Image.Image:
        """Resize and crop image to exact size maintaining aspect ratio"""
        target_width, target_height = size
        img.thumbnail((target_width * 2, target_height * 2), Image.Resampling.LANCZOS)
        
        # Crop to exact size from center
        width, height = img.size
        left = (width - target_width) / 2
        top = (height - target_height) / 2
        right = (width + target_width) / 2
        bottom = (height + target_height) / 2
        
        img = img.crop((left, top, right, bottom))
        return img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    def _create_gradient_background(self, width: int, height: int, category: str) -> Image.Image:
        """Create gradient background based on category"""
        from PIL import Image
        
        # Category-based color schemes
        color_schemes = {
            "Artist": [(100, 50, 150), (200, 100, 200)],
            "Cartoonist": [(255, 200, 100), (255, 150, 50)],
            "Sticker": [(100, 200, 255), (50, 150, 255)],
            "Realistic Image Store": [(240, 240, 250), (220, 220, 240)]
        }
        
        colors = color_schemes.get(category, [(240, 240, 250), (220, 220, 240)])
        
        img = Image.new('RGB', (width, height), colors[0])
        # Simple gradient effect
        for y in range(height):
            ratio = y / height
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        return img
    
    async def _generate_with_stability(self, prompt: str) -> str:
        """Generate image using Stability AI"""
        try:
            if not self.api_key:
                return None
            
            import asyncio
            import aiohttp
            
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("artifacts"):
                            # In production, you'd save the image and return a URL
                            # For now, return a placeholder
                            return self._save_generated_image(result["artifacts"][0].get("base64"))
            
            return None
        except Exception as e:
            print(f"Stability AI error: {str(e)}")
            return None
    
    async def _generate_with_openai(self, prompt: str) -> str:
        """Generate image using OpenAI DALL-E"""
        try:
            import openai
            import asyncio
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
            )
            
            return response.data[0].url
        except Exception as e:
            print(f"OpenAI DALL-E error: {str(e)}")
            return None
    
    async def _generate_with_replicate(self, prompt: str) -> str:
        """Generate image using Replicate"""
        try:
            import replicate
            import asyncio
            
            loop = asyncio.get_event_loop()
            output = await loop.run_in_executor(
                None,
                lambda: replicate.run(
                    "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                    input={"prompt": prompt}
                )
            )
            return output[0] if output else None
        except Exception as e:
            print(f"Replicate error: {str(e)}")
            return None
    
    def _create_placeholder_image(self, product_info: Dict[str, Any], variation: int = 0) -> str:
        """Create a placeholder image when API is not available"""
        try:
            # Create a simple placeholder image
            img = Image.new('RGB', (1024, 1024), color=(240, 240, 250))
            
            # Save to bytes
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Convert to base64 data URL
            import base64
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
            return f"data:image/png;base64,{img_base64}"
        except Exception as e:
            print(f"Error creating placeholder image: {str(e)}")
            # Return a minimal valid data URL
            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    def _save_generated_image(self, base64_data: str) -> str:
        """Convert base64 image to data URL"""
        if base64_data:
            return f"data:image/png;base64,{base64_data}"
        return None

