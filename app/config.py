"""
Configuration module for the WhatsApp AI Bot.
Loads all settings from environment variables with sensible defaults.
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from .env file or environment variables."""

    # ==========================================
    # WhatsApp Business API Settings
    # ==========================================
    WHATSAPP_TOKEN: str = ""  # Your Meta access token
    WHATSAPP_PHONE_NUMBER_ID: str = ""  # Your WhatsApp phone number ID
    WHATSAPP_VERIFY_TOKEN: str = ""  # Webhook verification token
    WHATSAPP_API_VERSION: str = "v18.0"  # Meta Graph API version

    # ==========================================
    # AI Provider API Keys (Free Tiers)
    # ==========================================
    GROQ_API_KEY: Optional[str] = None  # https://console.groq.com
    GEMINI_API_KEY: Optional[str] = None  # https://aistudio.google.com/app/apikey
    OPENAI_API_KEY: Optional[str] = None  # https://platform.openai.com

    # ==========================================
    # Bot Personality & Behavior
    # ==========================================
    BOT_NAME: str = "Dawinix"  # Name used for @mentions in groups
    BOT_PERSONALITY: str = """You are HaitianBot, a warm, playful, and intelligent AI assistant 
    chatting on WhatsApp. You speak like a knowledgeable friend — not too formal, not too casual. 
    You uplift the user, give real substance (not fluff), and aren't afraid to be a little witty. 
    You love helping people learn, brainstorm, and solve problems. Keep responses concise but 
    valuable since this is WhatsApp. Use emojis naturally but not excessively."""

    # ==========================================
    # Memory & Conversation Settings
    # ==========================================
    MAX_HISTORY_MESSAGES: int = 20  # How many messages to remember per chat
    ENABLE_LONG_TERM_MEMORY: bool = True  # Remember facts across sessions

    # ==========================================
    # Media & Image Generation
    # ==========================================
    IMAGE_GENERATION_PROVIDER: str = "gemini"  # "gemini" or "none"
    MAX_IMAGE_SIZE_MB: int = 5  # Max image size to process

    # ==========================================
    # Safety & Limits
    # ==========================================
    MAX_RESPONSE_LENGTH: int = 1500  # WhatsApp message limit consideration
    ENABLE_SAFETY_CHECKS: bool = True

    # ==========================================
    # Server Settings
    # ==========================================
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()

# Validate critical settings on import
def validate_settings():
    """Check that required settings are configured."""
    missing = []

    if not settings.WHATSAPP_TOKEN:
        missing.append("WHATSAPP_TOKEN")
    if not settings.WHATSAPP_PHONE_NUMBER_ID:
        missing.append("WHATSAPP_PHONE_NUMBER_ID")
    if not settings.WHATSAPP_VERIFY_TOKEN:
        missing.append("WHATSAPP_VERIFY_TOKEN")

    # Check at least one AI provider is configured
    ai_providers = [
        settings.GROQ_API_KEY,
        settings.GEMINI_API_KEY, 
        settings.OPENAI_API_KEY
    ]
    if not any(ai_providers):
        missing.append("At least one AI API key (GROQ_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY)")

    if missing:
        print(f"⚠️  Missing required settings: {', '.join(missing)}")
        print("   Please check your .env file")
    else:
        print("✅ All required settings loaded successfully!")

    return len(missing) == 0
