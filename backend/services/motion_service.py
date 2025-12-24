import os
from typing import Dict, Any
import base64
from io import BytesIO
from PIL import Image


class MotionService:
    def __init__(self):
        self.api_key = os.getenv("MOTION_EFFECT_API_KEY")
        self.provider = os.getenv("MOTION_EFFECT_PROVIDER", "stability").lower()
    
    async def generate_motion_effect(
        self,
        image_data: bytes,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate motion effects from an image.
        """
        try:
            if self.provider == "stability":
                result = await self._generate_with_stability(image_data, analysis)
            elif self.provider == "runway":
                result = await self._generate_with_runway(image_data, analysis)
            elif self.provider == "replicate":
                result = await self._generate_with_replicate(image_data, analysis)
            else:
                # Fallback: return original with effect applied
                result = self._apply_simple_effect(image_data)
            
            return {
                "url": result.get("url"),
                "download_url": result.get("url")
            }
        
        except Exception as e:
            print(f"Error generating motion effect: {str(e)}")
            # Return original image as fallback
            return {
                "url": self._image_to_data_url(image_data),
                "download_url": self._image_to_data_url(image_data)
            }
    
    async def _generate_with_stability(self, image_data: bytes, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate motion effect using Stability AI"""
        try:
            if not self.api_key:
                return self._apply_simple_effect(image_data)
            
            # Stability AI image-to-image or animation API
            # Note: This is a placeholder - actual implementation depends on Stability AI's API
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # For now, apply a simple effect
            return self._apply_simple_effect(image_data)
        
        except Exception as e:
            print(f"Stability motion error: {str(e)}")
            return self._apply_simple_effect(image_data)
    
    async def _generate_with_runway(self, image_data: bytes, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate motion effect using Runway ML"""
        try:
            if not self.api_key:
                return self._apply_simple_effect(image_data)
            
            # Runway ML API implementation
            # Placeholder for actual API integration
            return self._apply_simple_effect(image_data)
        
        except Exception as e:
            print(f"Runway ML error: {str(e)}")
            return self._apply_simple_effect(image_data)
    
    async def _generate_with_replicate(self, image_data: bytes, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate motion effect using Replicate"""
        try:
            import replicate
            import asyncio
            
            # Upload image first
            image_url = self._image_to_data_url(image_data)
            
            loop = asyncio.get_event_loop()
            output = await loop.run_in_executor(
                None,
                lambda: replicate.run(
                    "anotherjesse/zeroscope-v2-xl:9f6f602cd9b8d11b689c67c87b44b18fc4c40b9e",
                    input={
                        "image": image_url,
                        "prompt": f"Motion effect for {analysis.get('category', 'image')}"
                    }
                )
            )
            
            return {"url": output[0] if output else self._image_to_data_url(image_data)}
        
        except Exception as e:
            print(f"Replicate error: {str(e)}")
            return self._apply_simple_effect(image_data)
    
    def _apply_simple_effect(self, image_data: bytes) -> Dict[str, Any]:
        """Apply visual effects to simulate motion/animation"""
        try:
            from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
            import numpy as np
            
            img = Image.open(BytesIO(image_data))
            original_format = img.format or 'PNG'
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Apply motion-like effects
            # 1. Enhance brightness and contrast for dynamic look
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.15)
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Saturation(img)
            img = enhancer.enhance(1.2)
            
            # 2. Apply subtle motion blur effect
            img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # 3. Add slight sharpening to maintain clarity
            img = img.filter(ImageFilter.SHARPEN)
            
            # 4. Add a subtle glow effect (simulate motion trails)
            glow = img.copy()
            glow = glow.filter(ImageFilter.GaussianBlur(radius=2))
            glow = Image.blend(img, glow, 0.3)
            
            # Blend the glow with original
            final_img = Image.blend(img, glow, 0.7)
            
            # Convert back to bytes
            output = BytesIO()
            final_img.save(output, format='PNG', quality=95)
            output.seek(0)
            
            return {"url": self._image_to_data_url(output.read())}
        
        except Exception as e:
            print(f"Motion effect error: {str(e)}")
            import traceback
            traceback.print_exc()
            # Return original image with basic enhancement as fallback
            try:
                from PIL import Image, ImageEnhance
                img = Image.open(BytesIO(image_data))
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.1)
                output = BytesIO()
                img.save(output, format='PNG')
                output.seek(0)
                return {"url": self._image_to_data_url(output.read())}
            except:
                return {"url": self._image_to_data_url(image_data)}
    
    def _image_to_data_url(self, image_data: bytes) -> str:
        """Convert image bytes to data URL"""
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        return f"data:image/png;base64,{image_base64}"

