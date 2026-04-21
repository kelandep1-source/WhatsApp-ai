"""
Main FastAPI application for WhatsApp AI Bot.
Handles webhooks, message processing, and AI responses.
"""
import os
import json
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config import settings, validate_settings
from app.models.database import (
    init_db, get_db, add_conversation_message, 
    get_conversation_history, get_user_memories
)
from app.services.whatsapp import whatsapp_client
from app.services.ai_fallback import ai_service
from app.services.image_gen import image_service
from app.utils.safety import check_safety

# Initialize FastAPI app
app = FastAPI(
    title="WhatsApp AI Bot",
    description="AI-powered WhatsApp assistant with multi-provider fallback",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and validate settings on startup."""
    init_db()
    validate_settings()
    print("🚀 WhatsApp AI Bot started!")

# ==========================================
# Webhook Endpoints
# ==========================================

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    GET /webhook - Meta verification endpoint.
    Meta sends a challenge here to verify your webhook URL.
    """
    params = dict(request.query_params)

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    # Verify token matches our configured token
    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        print(f"✅ Webhook verified! Challenge: {challenge}")
        return Response(content=challenge, media_type="text/plain")
    else:
        print(f"❌ Webhook verification failed. Mode: {mode}, Token match: {token == settings.WHATSAPP_VERIFY_TOKEN}")
        raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    """
    POST /webhook - Receives all WhatsApp events (messages, status updates).
    This is where incoming messages are processed.
    """
    try:
        body = await request.json()

        # Parse the incoming message
        message_data = whatsapp_client.parse_incoming_message(body)

        if not message_data:
            # Not a message event (could be delivery/read receipt)
            return JSONResponse(content={"status": "ok"})

        # Extract message details
        phone_number = message_data["phone_number"]
        name = message_data["name"]
        message_id = message_data["message_id"]
        msg_type = message_data["type"]
        content = message_data["content"]
        is_group = message_data["is_group"]
        group_id = message_data["group_id"]

        print(f"📩 Message from {name} ({phone_number}): {content[:50]}...")

        # Mark message as read immediately
        try:
            await whatsapp_client.mark_as_read(message_id)
        except Exception as e:
            print(f"Could not mark as read: {e}")

        # Skip non-text messages for now (images, audio, etc.)
        # You can extend this to handle media
        if msg_type != "text":
            await whatsapp_client.send_text_message(
                phone_number,
                "I can currently only process text messages! 📱 "
                "Image and voice support coming soon."
            )
            return JSONResponse(content={"status": "ok"})

        # Check if we should respond to group messages
        if is_group:
            if not whatsapp_client.should_respond_to_group_message(content):
                print("⏭️ Group message without @mention - ignoring")
                return JSONResponse(content={"status": "ok"})
            else:
                # Remove @botname from content before processing
                import re
                content = re.sub(rf"@{settings.BOT_NAME}\s*", "", content, flags=re.IGNORECASE).strip()

        # ==========================================
        # Safety Check
        # ==========================================
        is_safe, violation_category, refusal_msg = check_safety(content)

        if not is_safe:
            print(f"🛡️ Blocked {violation_category} request from {phone_number}")
            await whatsapp_client.send_text_message(phone_number, refusal_msg)
            return JSONResponse(content={"status": "blocked"})

        # ==========================================
        # Check for Image Generation Request
        # ==========================================
        if image_service.is_image_request(content):
            prompt = image_service.extract_image_prompt(content)
            await whatsapp_client.send_text_message(
                phone_number,
                f"🎨 Generating image: *{prompt}*... This may take a moment!"
            )

            image_url = await image_service.generate_image(prompt)
            if image_url:
                await whatsapp_client.send_image_message(phone_number, image_url, caption=f"Generated: {prompt}")
            else:
                await whatsapp_client.send_text_message(
                    phone_number,
                    "😅 I couldn't generate that image right now. "
                    "Let's try again later or I can describe what it might look like!"
                )
            return JSONResponse(content={"status": "ok"})

        # ==========================================
        # Build Conversation Context
        # ==========================================
        conversation_id = group_id if group_id else phone_number

        # Get recent conversation history
        history = get_conversation_history(db, conversation_id, limit=settings.MAX_HISTORY_MESSAGES)
        history.reverse()  # Oldest first

        # Format messages for AI
        messages = []
        for msg in history:
            role = "user" if msg.role == "user" else "assistant"
            messages.append({"role": role, "content": msg.content})

        # Add current message
        messages.append({"role": "user", "content": content})

        # Get long-term memory if enabled
        memory_context = ""
        if settings.ENABLE_LONG_TERM_MEMORY:
            memories = get_user_memories(db, phone_number)
            if memories:
                memory_lines = [f"- {m.key}: {m.value}" for m in memories]
                memory_context = "\nThings you remember about this user:\n" + "\n".join(memory_lines)

        # Build system prompt with personality and memory
        system_prompt = f"""{settings.BOT_PERSONALITY}

{memory_context}

Important guidelines:
- Keep responses concise (under 1500 chars) for WhatsApp
- Be warm and helpful, use emojis naturally
- If you don't know something, say so honestly
- Never give medical, financial, or legal advice
- For complex topics, break into digestible chunks"""

        # ==========================================
        # Get AI Response
        # ==========================================
        ai_response = await ai_service.chat(messages, system_prompt)

        if ai_response.success:
            response_text = ai_response.text

            # Save conversation to database
            add_conversation_message(db, phone_number, conversation_id, "user", content)
            add_conversation_message(db, phone_number, conversation_id, "assistant", response_text)

            # Send response back to WhatsApp
            await whatsapp_client.send_text_message(phone_number, response_text, reply_to=message_id)

            print(f"✅ Replied to {name} using {ai_response.provider}")
        else:
            # AI failed entirely
            await whatsapp_client.send_text_message(
                phone_number,
                "🧠 Oops, my brain is a bit overloaded right now. "
                "Mind trying again in a few seconds?"
            )

        return JSONResponse(content={"status": "ok"})

    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

# ==========================================
# Health Check & Info Endpoints
# ==========================================

@app.get("/")
async def root():
    """Root endpoint - basic info."""
    return {
        "name": "WhatsApp AI Bot",
        "version": "1.0.0",
        "status": "running",
        "bot_name": settings.BOT_NAME,
        "providers_configured": [
            "groq" if settings.GROQ_API_KEY else None,
            "gemini" if settings.GEMINI_API_KEY else None,
            "openai" if settings.OPENAI_API_KEY else None
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# ==========================================
# Manual Testing Endpoints (Development Only)
# ==========================================

@app.post("/test/send")
async def test_send_message(to: str, message: str):
    """Manually send a message (for testing)."""
    try:
        result = await whatsapp_client.send_text_message(to, message)
        return {"status": "sent", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
