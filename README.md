# 🤖 WhatsApp AI Bot — Complete Setup Guide

A warm, intelligent AI assistant for WhatsApp with multi-provider AI fallback, conversation memory, group chat support, and safety filtering.

---

## 📁 Project Structure

```
whatsapp-ai-bot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & webhook endpoints
│   ├── config.py            # Settings & environment variables
│   ├── services/
│   │   ├── __init__.py
│   │   ├── whatsapp.py      # WhatsApp Cloud API client
│   │   ├── ai_fallback.py   # Multi-provider AI with automatic fallback
│   │   └── image_gen.py     # Image generation service
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py      # SQLite models & memory storage
│   └── utils/
│       ├── __init__.py
│       └── safety.py        # Content filtering & safety checks
├── .env.example
├── requirements.txt
├── Dockerfile
├── railway.toml
└── README.md                # This file
```

---

## 🚀 Quick Start (Step-by-Step)

### Step 1: Get Your Free AI API Keys

You need **at least one** of these. More = better fallback.

| Provider | Free Tier | Get Key At | Rate Limit |
|----------|-----------|------------|------------|
| **Groq** (Llama 4) | Generous daily limits | [console.groq.com](https://console.groq.com) | 20 req/min |
| **Gemini** (Google) | 60 req/min | [aistudio.google.com](https://aistudio.google.com/app/apikey) | 60 req/min |
| **OpenAI** | Requires credits | [platform.openai.com](https://platform.openai.com) | Pay-per-use |

> 💡 **Recommendation**: Start with Groq + Gemini. Groq is fastest, Gemini is most capable. OpenAI is optional backup.

### Step 2: Set Up Meta WhatsApp Business API

#### 2.1 Create a Meta Developer Account
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **"Get Started"** and create/login to your account
3. Verify your account with a phone number

#### 2.2 Create a WhatsApp App
1. Go to **My Apps** → **Create App**
2. Select **"Business"** as app type
3. Give it a name (e.g., "HaitianBot")
4. **Important**: You do NOT need a Business Manager account for testing

#### 2.3 Add WhatsApp Product
1. In your app dashboard, click **"Add Product"**
2. Find **WhatsApp** and click **"Set Up"**

#### 2.4 Get Your Credentials
In the WhatsApp → **Getting Started** section, you'll see:

- **Access Token** → Copy this → `WHATSAPP_TOKEN`
- **Phone Number ID** → Copy this → `WHATSAPP_PHONE_NUMBER_ID`

> ⚠️ The default token expires in 24 hours! For production, generate a **Permanent Token**:
> 1. Go to [business.facebook.com](https://business.facebook.com)
> 2. Settings → System Users → Add
> 3. Generate Token with `whatsapp_business_messaging` permission

#### 2.5 Add a Test Phone Number
1. In the WhatsApp dashboard, go to **Phone Numbers**
2. Click **"Add Phone Number"** or use the default test number
3. Verify it via SMS or voice call
4. You can message this number from your personal WhatsApp to test

### Step 3: Deploy Your Bot

#### Option A: Railway (Recommended — Easiest)

1. **Install Railway CLI** (or use the web dashboard):
   ```bash
   npm install -g @railway/cli
   ```

2. **Create a new project**:
   ```bash
   railway login
   railway init
   ```

3. **Set environment variables**:
   ```bash
   railway variables set WHATSAPP_TOKEN="your_token"
   railway variables set WHATSAPP_PHONE_NUMBER_ID="your_id"
   railway variables set WHATSAPP_VERIFY_TOKEN="random_string_123"
   railway variables set GROQ_API_KEY="your_groq_key"
   railway variables set GEMINI_API_KEY="your_gemini_key"
   railway variables set BOT_NAME="HaitianBot"
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

5. **Get your public URL**:
   ```bash
   railway domain
   ```
   Copy the URL — you'll need it for the webhook.

#### Option B: Replit

1. Go to [replit.com](https://replit.com) and create a new Python Repl
2. Upload all project files
3. Create a `.env` file with your variables
4. In the **Shell** tab, run:
   ```bash
   pip install -r requirements.txt
   ```
5. Click **Run** — Replit gives you a public URL automatically

#### Option C: Local Development (with ngrok)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file**:
   ```bash
   cp .env.example .env
   # Edit .env with your real values
   ```

3. **Run locally**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **Expose with ngrok**:
   ```bash
   ngrok http 8000
   ```
   Copy the `https://` URL for the webhook.

### Step 4: Configure the Webhook in Meta Dashboard

1. Go to your Meta App → **WhatsApp** → **Configuration**
2. Find **Webhooks** section → Click **"Edit"**
3. In **Callback URL**, paste your public URL + `/webhook`:
   ```
   https://your-app.railway.app/webhook
   ```
4. In **Verify Token**, enter the same random string you put in `.env`:
   ```
   your_random_verify_token_here
   ```
5. Click **"Verify and Save"**
6. Under **Webhook Fields**, click **"Manage"** and subscribe to:
   - ✅ `messages`
   - ✅ `message_deliveries` (optional)

### Step 5: Test Your Bot! 🎉

1. Open WhatsApp on your phone
2. Send a message to your test phone number
3. You should get an AI response within 2-5 seconds!

**Try these messages:**
- `"Hey, what's up?"`
- `"Explain quantum computing like I'm 5"`
- `"@HaitianBot what do you think about AI?"` (in groups)
- `"Generate an image of a cat astronaut"`

---

## 🛡️ Safety Features

The bot automatically refuses:
- 🏥 Medical advice requests
- 💰 Financial/investment advice
- ⚖️ Legal advice
- 🚫 Illegal activities
- 🔞 Inappropriate content

It responds with friendly, helpful alternatives instead.

---

## 💰 Cost Breakdown (~1,000 Conversations/Month)

| Component | Provider | Cost |
|-----------|----------|------|
| **AI (Text)** | Groq Free Tier | **$0** |
| **AI (Fallback)** | Gemini Free Tier | **$0** |
| **Hosting** | Railway (Hobby) | **$5/month** |
| **WhatsApp API** | Meta (1st 1,000 convos) | **$0** |
| **Image Gen** | Gemini (if available) | **$0** |
| **Total** | | **~$5/month** |

> 📌 After 1,000 conversations, Meta charges ~$0.005-0.008 per conversation. At 2,000/month, add ~$5-8.

---

## 🔧 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `WHATSAPP_TOKEN` | ✅ | Meta WhatsApp access token |
| `WHATSAPP_PHONE_NUMBER_ID` | ✅ | Your WhatsApp phone number ID |
| `WHATSAPP_VERIFY_TOKEN` | ✅ | Random string for webhook verification |
| `GROQ_API_KEY` | ⚠️ | Groq API key (free tier) |
| `GEMINI_API_KEY` | ⚠️ | Google Gemini API key (free tier) |
| `OPENAI_API_KEY` | ❌ | OpenAI API key (optional backup) |
| `BOT_NAME` | ❌ | Bot name for @mentions (default: HaitianBot) |
| `MAX_HISTORY_MESSAGES` | ❌ | Messages to remember (default: 20) |
| `ENABLE_LONG_TERM_MEMORY` | ❌ | Remember facts across sessions (default: true) |
| `IMAGE_GENERATION_PROVIDER` | ❌ | "gemini" or "none" (default: gemini) |

---

## 🐛 Troubleshooting

### "Webhook verification failed"
- Make sure your `WHATSAPP_VERIFY_TOKEN` matches exactly in both `.env` and Meta dashboard
- Check that your URL is publicly accessible (not localhost)

### "No AI providers configured"
- Add at least one API key (GROQ_API_KEY or GEMINI_API_KEY)
- Restart the server after editing `.env`

### "Rate limited"
- The bot will automatically fall back to the next provider
- Consider adding more providers for better resilience

### "Messages not being received"
- Check Meta dashboard → Webhooks → Recent Deliveries
- Make sure you've subscribed to the `messages` field
- Verify your phone number is active in the dashboard

### "Bot responds in groups to everything"
- Make sure `BOT_NAME` matches exactly (case-insensitive check)
- Users must type `@BotName` (e.g., `@HaitianBot`)

---

## 🚀 Going Live (Meta Business Verification)

For production use beyond testing:

1. **Verify your business** at [business.facebook.com](https://business.facebook.com)
2. **Add a real phone number** (not test number) to WhatsApp Business
3. **Complete Business Verification** in Meta Business Manager
4. **Submit for review** if needed (usually automatic for messaging)
5. **Display Name**: Choose a name users will see (e.g., "HaitianBot")

> ⏱️ Business verification can take 1-5 business days.

---

## 🎨 Customizing Your Bot

### Change Personality
Edit `app/config.py` → `BOT_PERSONALITY`:
```python
BOT_PERSONALITY: str = """You are [YourBotName], a [trait] AI assistant..."""
```

### Add More AI Providers
Edit `app/services/ai_fallback.py` → add a new class inheriting from `AIProvider`.

### Enable/Disable Features
Edit `.env`:
```bash
ENABLE_LONG_TERM_MEMORY=false    # Turn off long-term memory
IMAGE_GENERATION_PROVIDER=none   # Disable image generation
```

---

## 📜 License

MIT License — use it, modify it, sell it, whatever. Just don't use it for evil. ✌️

---

**Built with ❤️ by you, powered by free AI APIs.**

Questions? Check the troubleshooting section or search your error message online — the WhatsApp API community is huge!
