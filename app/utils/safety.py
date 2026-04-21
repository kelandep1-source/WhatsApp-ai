"""
Safety module for content filtering and policy enforcement.
Prevents medical, financial, legal advice and illegal requests.
"""
import re
from typing import Tuple, Optional

# Categories of advice we should NOT provide
RESTRICTED_CATEGORIES = {
    "medical": [
        r"\b(diagnos(?:is|e)|symptoms? of|treat(?:ment)? for|cure for|medicine for|pill for|drug for|prescription)",
        r"\b(should i take|is it safe to|can i eat|pregnant and|covid|vaccine|cancer|diabetes|heart attack)",
        r"\b(i feel sick|i have pain|my doctor|hospital|emergency|urgent care|therapy for|mental health diagnosis)",
    ],
    "financial": [
        r"\b(invest in|stock tip|buy stock|sell stock|crypto|bitcoin|trading advice|portfolio|retirement plan)",
        r"\b(should i buy|should i sell|market prediction|financial advice|tax strategy|loan approval|credit score fix)",
        r"\b(forex|day trading|margin|options trading|insurance recommendation|mortgage advice|debt relief)",
    ],
    "legal": [
        r"\b(lawsuit|sue|court|lawyer|attorney|legal advice|contract review|terms of service|copyright|patent)",
        r"\b(immigration|visa|green card|citizenship|divorce|custody|will|estate|criminal charge|arrested)",
        r"\b(my rights|am i liable|can they sue|is it illegal to|legal consequences|statute of limitations)",
    ],
    "illegal": [
        r"\b(hack|crack|steal|rob|kill|hurt|harm|weapon|bomb|drug deal|counterfeit|fraud|scam|phishing)",
        r"\b(how to make|recipe for|synthesize|manufacture)\s+(?:bomb|drug|meth|explosive|poison)",
        r"\b(child|minor)\s+(?:porn|explicit|nude)",
        r"\b(credit card|ssn|social security|password)\s+(?:steal|hack|generate|fake)",
    ]
}

# Harmless alternatives we CAN discuss
ALLOWED_TOPICS = [
    r"\b(general information about|what is|how does|history of|explain|compare|difference between)",
    r"\b(brainstorm|ideas for|creative|writing|coding|learning|study|homework help|tutor|explain like i'm)",
]

REFUSAL_MESSAGES = {
    "medical": (
        "🩺 I can't provide medical advice, diagnoses, or treatment recommendations. "
        "Your health is too important! Please consult a qualified healthcare provider "
        "for any medical concerns. I'm happy to explain general health concepts or "
        "help you find reputable health resources though! 💙"
    ),
    "financial": (
        "💰 I can't give financial, investment, or tax advice. Money matters are serious! "
        "Please speak with a certified financial advisor or tax professional. "
        "I'd love to help you budget, learn about economics, or brainstorm side hustle ideas instead! 📊"
    ),
    "legal": (
        "⚖️ I can't provide legal advice or interpret laws for specific situations. "
        "Legal matters need a licensed attorney! I'm happy to explain general legal concepts, "
        "help you understand terminology, or assist with drafting non-legal documents though. 📚"
    ),
    "illegal": (
        "🚫 I can't help with anything illegal or harmful. Let's keep things positive and lawful! "
        "I'm here to help with creative projects, learning, productivity, and good vibes only. ✨"
    ),
    "inappropriate": (
        "🌟 Let's keep our conversation friendly and appropriate for all ages! "
        "I'm happy to chat about hobbies, learning, creativity, tech, and tons of other topics. What would you like to explore? 😊"
    )
}

def check_safety(message: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Check if a message contains restricted content.

    Returns:
        (is_safe, category, refusal_message)
        - is_safe: True if message is okay to process
        - category: The violation category if unsafe, None otherwise
        - refusal_message: Response to send if unsafe, None otherwise
    """
    message_lower = message.lower()

    # Check for restricted categories
    for category, patterns in RESTRICTED_CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return False, category, REFUSAL_MESSAGES[category]

    # Check for inappropriate content (simplified - production should use stronger filtering)
    inappropriate_words = [
        r"\b(f+u+c+k+|s+h+i+t+|b+i+t+c+h+|a+s+s+h+o+l+e+)",
        r"\b(n+i+g+g+e+r+|r+e+t+a+r+d+|f+a+g+g+o+t+)",
    ]
    for pattern in inappropriate_words:
        if re.search(pattern, message_lower, re.IGNORECASE):
            return False, "inappropriate", REFUSAL_MESSAGES["inappropriate"]

    return True, None, None

def sanitize_for_display(text: str) -> str:
    """Clean text for safe display in WhatsApp."""
    # Remove potentially harmful characters
    text = text.replace("\x00", "")  # Null bytes
    text = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]", "", text)  # Control chars
    return text.strip()

def format_safe_response(text: str, max_length: int = 1500) -> str:
    """Format and truncate response for WhatsApp safety."""
    text = sanitize_for_display(text)
    if len(text) > max_length:
        text = text[:max_length-3] + "..."
    return text
