"""
Image generation service using available AI providers.
Currently supports Gemini for image generation.
"""
import os
import uuid
from typing import Optional
import httpx
from app.config import settings

class ImageGenerationService:
    """Service for generating images from text prompts."""

    def __init__(self):
        self.provider = settings.IMAGE_GENERATION_PROVIDER
        self.output_dir = "data/generated_images"
        os.makedirs(self.output_dir, exist_ok=True)

    async def generate_image(self, prompt: str) -> Optional[str]:
        """
        Generate an image from text prompt.
        Returns the URL/path of the generated image.

        Note: Full implementation depends on your chosen provider's capabilities.
        This is a framework you can extend.
        """
        if self.provider == "none":
            return None

        if self.provider == "gemini" and settings.GEMINI_API_KEY:
            return await self._generate_with_gemini(prompt)

        return None

    async def _generate_with_gemini(self, prompt: str) -> Optional[str]:
        """Generate image using Gemini (experimental feature)."""
        try:
            # Note: As of 2026, Gemini's image generation may require specific models
            # This is a template implementation

            payload = {
                "contents": [{
                    "role": "user",
                    "parts": [{"text": f"Create an image of: {prompt}"}]
                }],
                "generationConfig": {
                    "responseModalities": ["Text", "Image"]
                }
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent",
                    params={"key": settings.GEMINI_API_KEY},
                    json=payload
                )

                if response.status_code != 200:
                    print(f"Gemini image gen failed: {response.status_code}")
                    return None

                # Parse response - actual implementation depends on API format
                data = response.json()

                # Save image if present in response
                # This is simplified - actual implementation needed
                return None

        except Exception as e:
            print(f"Image generation error: {e}")
            return None

    def is_image_request(self, text: str) -> bool:
        """Check if user is asking for image generation."""
        triggers = [
            r"generate (an? )?image",
            r"create (an? )?image",
            r"draw (a |an )?",
            r"make (a |an )?picture",
            r"image of",
            r"photo of",
            r"/image",
            r"/generate"
        ]

        import re
        text_lower = text.lower()
        for trigger in triggers:
            if re.search(trigger, text_lower):
                return True
        return False

    def extract_image_prompt(self, text: str) -> str:
        """Extract the image prompt from user's message."""
        import re

        # Remove trigger words
        patterns = [
            r"^(?:generate|create|draw|make)\s+(?:an?\s+)?image\s+(?:of\s+)?",
            r"^(?:generate|create|draw|make)\s+(?:a\s+)?picture\s+(?:of\s+)?",
            r"^/image\s+",
            r"^/generate\s+",
        ]

        prompt = text
        for pattern in patterns:
            prompt = re.sub(pattern, "", prompt, flags=re.IGNORECASE)

        return prompt.strip()

# Create global instance
image_service = ImageGenerationService()
