"""
AI service with multi-provider fallback system.
Tries providers in order: Groq (Llama 4) -> Gemini -> OpenAI
If one fails or rate-limits, automatically tries the next.
"""
import os
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import httpx

from app.config import settings
from app.utils.safety import format_safe_response

@dataclass
class AIResponse:
    """Standardized response from any AI provider."""
    text: str
    provider: str
    model: str
    success: bool
    error: Optional[str] = None

class AIProvider:
    """Base class for AI providers."""

    async def chat(self, messages: List[Dict[str, str]], 
                   system_prompt: str = "") -> AIResponse:
        raise NotImplementedError

    async def generate_image(self, prompt: str) -> Optional[str]:
        """Generate image and return URL. Returns None if not supported."""
        return None

class GroqProvider(AIProvider):
    """Groq provider with Llama 4 (free tier available)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"  # Latest Llama 4
        self.fallback_model = "llama3-70b-8192"  # Fallback if Llama 4 unavailable

    async def chat(self, messages: List[Dict[str, str]], 
                   system_prompt: str = "") -> AIResponse:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "system", "content": system_prompt}] + messages,
                "temperature": 0.8,
                "max_tokens": 1500,
                "top_p": 0.9
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 429:  # Rate limited
                    return AIResponse(
                        text="", provider="groq", model=self.model,
                        success=False, error="rate_limited"
                    )

                response.raise_for_status()
                data = response.json()

                text = data["choices"][0]["message"]["content"]
                return AIResponse(
                    text=text, provider="groq", model=self.model, success=True
                )

        except Exception as e:
            return AIResponse(
                text="", provider="groq", model=self.model,
                success=False, error=str(e)
            )

class GeminiProvider(AIProvider):
    """Google Gemini provider (free tier: 60 req/min)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "gemini-2.5-pro-exp-03-25"  # Latest Gemini 2.5 Pro

    async def chat(self, messages: List[Dict[str, str]], 
                   system_prompt: str = "") -> AIResponse:
        try:
            # Convert messages to Gemini format
            gemini_messages = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                gemini_messages.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })

            payload = {
                "contents": gemini_messages,
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "generationConfig": {
                    "temperature": 0.8,
                    "maxOutputTokens": 1500,
                    "topP": 0.9
                }
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent",
                    params={"key": self.api_key},
                    json=payload
                )

                if response.status_code == 429:
                    return AIResponse(
                        text="", provider="gemini", model=self.model,
                        success=False, error="rate_limited"
                    )

                response.raise_for_status()
                data = response.json()

                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return AIResponse(
                    text=text, provider="gemini", model=self.model, success=True
                )

        except Exception as e:
            return AIResponse(
                text="", provider="gemini", model=self.model,
                success=False, error=str(e)
            )

    async def generate_image(self, prompt: str) -> Optional[str]:
        """Generate image using Gemini (if supported in your tier)."""
        try:
            payload = {
                "contents": [{
                    "role": "user",
                    "parts": [{"text": f"Generate an image: {prompt}"}]
                }],
                "generationConfig": {
                    "responseModalities": ["Text", "Image"]
                }
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent",
                    params={"key": self.api_key},
                    json=payload
                )

                if response.status_code != 200:
                    return None

                data = response.json()
                # Note: Actual image extraction depends on Gemini's response format
                # This is a simplified version
                return None  # Placeholder - implement based on actual API response

        except Exception as e:
            print(f"Image generation error: {e}")
            return None

class OpenAIProvider(AIProvider):
    """OpenAI provider (GPT-4o) - requires credits."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "gpt-4o"

    async def chat(self, messages: List[Dict[str, str]], 
                   system_prompt: str = "") -> AIResponse:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "system", "content": system_prompt}] + messages,
                "temperature": 0.8,
                "max_tokens": 1500,
                "top_p": 0.9
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 429:
                    return AIResponse(
                        text="", provider="openai", model=self.model,
                        success=False, error="rate_limited"
                    )

                response.raise_for_status()
                data = response.json()

                text = data["choices"][0]["message"]["content"]
                return AIResponse(
                    text=text, provider="openai", model=self.model, success=True
                )

        except Exception as e:
            return AIResponse(
                text="", provider="openai", model=self.model,
                success=False, error=str(e)
            )

class AIFallbackService:
    """
    Manages multiple AI providers with automatic fallback.
    Order: Groq -> Gemini -> OpenAI
    """

    def __init__(self):
        self.providers: List[AIProvider] = []

        # Initialize providers based on available API keys
        if settings.GROQ_API_KEY:
            self.providers.append(GroqProvider(settings.GROQ_API_KEY))
            print("✅ Groq provider initialized")

        if settings.GEMINI_API_KEY:
            self.providers.append(GeminiProvider(settings.GEMINI_API_KEY))
            print("✅ Gemini provider initialized")

        if settings.OPENAI_API_KEY:
            self.providers.append(OpenAIProvider(settings.OPENAI_API_KEY))
            print("✅ OpenAI provider initialized")

        if not self.providers:
            raise ValueError("No AI providers configured! Please add at least one API key.")

    async def chat(self, messages: List[Dict[str, str]], 
                   system_prompt: str = "") -> AIResponse:
        """
        Send chat request with automatic fallback between providers.

        Args:
            messages: List of {role, content} dicts
            system_prompt: System instructions for the AI

        Returns:
            AIResponse with text and metadata
        """
        last_error = None

        for provider in self.providers:
            try:
                result = await provider.chat(messages, system_prompt)

                if result.success:
                    # Format response for WhatsApp
                    result.text = format_safe_response(result.text)
                    print(f"🤖 Response from {result.provider} ({result.model})")
                    return result
                else:
                    last_error = result.error
                    print(f"⚠️ {provider.__class__.__name__} failed: {result.error}")

                    # Don't retry on auth errors, only on rate limits/timeouts
                    if "auth" in result.error.lower() or "key" in result.error.lower():
                        continue

                    # Brief delay before trying next provider
                    await asyncio.sleep(0.5)

            except Exception as e:
                last_error = str(e)
                print(f"❌ {provider.__class__.__name__} error: {e}")
                continue

        # All providers failed
        return AIResponse(
            text="I'm having trouble connecting to my brain right now 🧠⚡ "
                 "Please try again in a moment!",
            provider="fallback",
            model="none",
            success=False,
            error=last_error
        )

    async def generate_image(self, prompt: str) -> Optional[str]:
        """Try to generate image using available providers."""
        for provider in self.providers:
            if hasattr(provider, 'generate_image'):
                try:
                    result = await provider.generate_image(prompt)
                    if result:
                        return result
                except Exception as e:
                    print(f"Image generation failed for {provider.__class__.__name__}: {e}")
                    continue
        return None

# Create global AI service instance
ai_service = AIFallbackService()
