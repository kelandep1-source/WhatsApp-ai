"""
WhatsApp Cloud API client for sending and receiving messages.
Handles all communication with Meta's WhatsApp Business Platform.
"""
import httpx
import json
from typing import Optional, Dict, Any, List
from app.config import settings

class WhatsAppClient:
    """Client for interacting with WhatsApp Cloud API."""

    def __init__(self):
        self.base_url = f"https://graph.facebook.com/{settings.WHATSAPP_API_VERSION}"
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }

    async def send_text_message(self, to: str, text: str, 
                                reply_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a text message to a WhatsApp user.

        Args:
            to: Recipient phone number (with country code, e.g., "14155551234")
            text: Message text content
            reply_to: Optional message ID to reply to
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"body": text[:4096]}  # WhatsApp text limit
        }

        if reply_to:
            payload["context"] = {"message_id": reply_to}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def send_image_message(self, to: str, image_url: str, 
                                  caption: Optional[str] = None,
                                  reply_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Send an image message.

        Args:
            to: Recipient phone number
            image_url: Publicly accessible URL of the image
            caption: Optional image caption
            reply_to: Optional message ID to reply to
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "image",
            "image": {"link": image_url}
        }

        if caption:
            payload["image"]["caption"] = caption[:1024]
        if reply_to:
            payload["context"] = {"message_id": reply_to}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def send_reaction(self, to: str, message_id: str, 
                            emoji: str = "👍") -> Dict[str, Any]:
        """Send a reaction to a message."""
        url = f"{self.base_url}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "reaction",
            "reaction": {
                "message_id": message_id,
                "emoji": emoji
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        """Mark an incoming message as read."""
        url = f"{self.base_url}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def get_media_url(self, media_id: str) -> str:
        """Get the URL for downloading media."""
        url = f"{self.base_url}/{media_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("url", "")

    async def download_media(self, media_url: str) -> bytes:
        """Download media content from WhatsApp."""
        async with httpx.AsyncClient() as client:
            response = await client.get(media_url, headers=self.headers)
            response.raise_for_status()
            return response.content

    def parse_incoming_message(self, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse incoming webhook payload to extract message details.

        Returns dict with:
        - phone_number: Sender's phone number
        - name: Sender's profile name
        - message_id: WhatsApp message ID
        - timestamp: Message timestamp
        - type: Message type (text, image, etc.)
        - content: Message content
        - is_group: Whether from group chat
        - group_id: Group ID if from group
        """
        try:
            entry = webhook_data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})

            if "messages" not in value:
                return None  # Not a message event (could be status update)

            message = value["messages"][0]
            contact = value.get("contacts", [{}])[0]

            # Determine if group message
            is_group = message.get("context", {}).get("group_id") is not None
            group_id = message.get("context", {}).get("group_id")

            # Extract content based on message type
            msg_type = message.get("type", "unknown")
            content = ""

            if msg_type == "text":
                content = message.get("text", {}).get("body", "")
            elif msg_type == "image":
                content = message.get("image", {}).get("caption", "")
            elif msg_type == "audio":
                content = "[Audio message]"
            elif msg_type == "video":
                content = message.get("video", {}).get("caption", "") or "[Video]"
            elif msg_type == "document":
                content = message.get("document", {}).get("caption", "") or "[Document]"
            elif msg_type == "location":
                loc = message.get("location", {})
                content = f"[Location: {loc.get('latitude')}, {loc.get('longitude')}]"
            else:
                content = f"[{msg_type}]"

            return {
                "phone_number": message.get("from"),
                "name": contact.get("profile", {}).get("name", "Unknown"),
                "message_id": message.get("id"),
                "timestamp": message.get("timestamp"),
                "type": msg_type,
                "content": content,
                "raw_message": message,
                "is_group": is_group,
                "group_id": group_id
            }

        except (KeyError, IndexError) as e:
            print(f"Error parsing webhook: {e}")
            return None

    def should_respond_to_group_message(self, message_text: str) -> bool:
        """
        Check if bot should respond to a group message.
        Only respond if tagged with @BotName.
        """
        if not message_text:
            return False

        bot_mention = f"@{settings.BOT_NAME.lower()}"
        return bot_mention in message_text.lower()

# Create global client instance
whatsapp_client = WhatsAppClient()
