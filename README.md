# 🤖 WhatsApp AI Bot — Complete Setup Guide

A warm, intelligent AI assistant for WhatsApp with multi-provider AI fallback, conversation memory, group chat support, safety filtering, and a full analytics dashboard.

---

## 📁 Project Structure

```
whatsapp-ai-bot/
├── app/                          # Backend (Python/FastAPI)
│   ├── __init__.py
│   ├── main.py                   # FastAPI app, webhooks & dashboard API
│   ├── config.py                 # Settings & environment variables
│   ├── services/
│   │   ├── __init__.py
│   │   ├── whatsapp.py           # WhatsApp Cloud API client
│   │   ├── ai_fallback.py        # Multi-provider AI with automatic fallback
│   │   └── image_gen.py          # Image generation service
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py           # SQLite models & memory storage
│   └── utils/
│       ├── __init__.py
│       └── safety.py             # Content filtering & safety checks
├── frontend/                     # Dashboard (Next.js/React)
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── postcss.config.js
│   ├── .env.local.example
│   ├── next-env.d.ts
│   └── src/
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx          # Main dashboard page
│       │   └── globals.css
│       ├── components/
│       │   ├── ui/card.tsx
│       │   ├── sidebar.tsx
│       │   ├── stats-cards.tsx
│       │   ├── activity-chart.tsx
│       │   ├── conversations-list.tsx
│       │   ├── logs-viewer.tsx
│       │   ├── settings-panel.tsx
│       │   ├── users-management.tsx
│       │   └── providers-status.tsx
│       ├── lib/
│       │   └── utils.ts
│       └── hooks/
├── .env.example
├── requirements.txt
├── Dockerfile
├── railway.toml
└── README.md                     # This file
```

---

## 🎨 Dashboard Features

| Feature | Description |
|---------|-------------|
| **📊 Overview** | Real-time stats, activity charts, recent conversations, system logs, provider status |
| **💬 Conversations** | View all chats, message counts, group detection, last activity |
| **📈 Analytics** | 7-day activity graphs, success rates, provider performance |
| **🛡️ System Logs** | Filter by level (info/warning/error/blocked), search, timestamps |
| **👥 Users** | Manage users, block/unblock, view activity, country detection |
| **⚙️ Settings** | Change bot name, personality, memory settings, toggle features live |
| **⚡ Providers** | Monitor Groq/Gemini/OpenAI status, response times, fallback tracking |

---

## 🚀 Quick Start (Step-by-Step)

### Step 1: Get Your Free AI API Keys

You need **at least one** of these. More = better fallback.

| Provider | Free Tier | Get Key At | Rate Limit |
|----------|-----------|------------|------------|
| **Groq** (Llama 4) | Generous daily limits | [console.groq.com](https://console.groq.com) | 20 req/min |
| **Gemini** (Google) | 60 req/min | [aistudio.google.com](https://aistudio.google.com/app/apikey) | 60 req/min |
| **OpenAI** | Requires credits | [platform.openai.com](https://platform.openai.com) | Pay-per-use |

> 💡 **Recommendation**: Start with Groq + Gemini. Groq is fastest, Gemini is most capable.

### Step 2: Set Up Meta WhatsApp Business API

#### 2.1 Create a Meta Developer Account
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **"Get Started"** and create/login to your account
3. Verify your account with a phone number

#### 2.2 Create a WhatsApp App
1. Go to **My Apps** → **Create App**
2. Select **"Business"** as app type
3. Give it a name (e.g., "HaitianBot")

#### 2.3 Add WhatsApp Product
1. In your app dashboard, click **"Add Product"**
2. Find **WhatsApp** and click **"Set Up"**

#### 2.4 Get Your Credentials
In the WhatsApp → **Getting Started** section:

- **Access Token** → `WHATSAPP_TOKEN`
- **Phone Number ID** → `WHATSAPP_PHONE_NUMBER_ID`

> ⚠️ The default token expires in 24 hours! For production, generate a **Permanent Token**:
> 1. Go to [business.facebook.com](https://business.facebook.com)
> 2. Settings → System Users → Add
> 3. Generate Token with `whatsapp_business_messaging` permission

#### 2.5 Add a Test Phone Number
1. In the WhatsApp dashboard, go to **Phone Numbers**
2. Click **"Add Phone Number"** or use the default test number
3. Verify it via SMS or voice call

### Step 3: Deploy Backend

#### Option A: Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Set environment variables
railway variables set WHATSAPP_TOKEN="your_token"
railway variables set WHATSAPP_PHONE_NUMBER_ID="your_id"
railway variables set WHATSAPP_VERIFY_TOKEN="random_string_123"
railway variables set GROQ_API_KEY="your_groq_key"
railway variables set GEMINI_API_KEY="your_gemini_key"
railway variables set BOT_NAME="HaitianBot"

# Get your public URL
railway domain
```

#### Option B: Local + ngrok (Testing)

```bash
# 1. Backend
cd whatsapp-ai-bot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. In another terminal, expose with ngrok
ngrok http 8000
# Copy the https:// URL for webhook
```

### Step 4: Configure Webhook in Meta Dashboard

1. Go to your Meta App → **WhatsApp** → **Configuration**
2. Find **Webhooks** → Click **"Edit"**
3. **Callback URL**: `https://your-app.railway.app/webhook`
4. **Verify Token**: Same random string from `.env`
5. Click **"Verify and Save"**
6. Subscribe to: ✅ `messages`

### Step 5: Deploy Dashboard (Optional)

#### Vercel (Recommended for Frontend)

```bash
cd frontend
npm install

# Create .env.local
cp .env.local.example .env.local
# Edit: NEXT_PUBLIC_API_URL=https://your-backend.railway.app

# Deploy to Vercel
npm install -g vercel
vercel
```

Or connect your GitHub repo to [vercel.com](https://vercel.com) for automatic deploys.

#### Local Development

```bash
cd frontend
npm install
npm run dev
# Dashboard at http://localhost:3000
```

### Step 6: Test Your Bot! 🎉

1. Open WhatsApp on your phone
2. Send a message to your test phone number
3. Check the dashboard for real-time updates!

---

## 💰 Cost Breakdown (~1,000 Conversations/Month)

| Component | Provider | Cost |
|-----------|----------|------|
| **AI (Text)** | Groq Free Tier | **$0** |
| **AI (Fallback)** | Gemini Free Tier | **$0** |
| **Backend Hosting** | Railway (Hobby) | **$5/month** |
| **Dashboard Hosting** | Vercel | **$0** |
| **WhatsApp API** | Meta (1st 1,000 convos) | **$0** |
| **Database** | SQLite (included) | **$0** |
| **Total** | | **~$5/month** |

> 📌 After 1,000 conversations, Meta charges ~$0.005-0.008 per conversation.

---

## 🔧 Environment Variables

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

| Problem | Solution |
|---------|----------|
| "Webhook verification failed" | Verify token matches exactly in `.env` and Meta dashboard |
| "No AI providers configured" | Add at least one API key (GROQ_API_KEY or GEMINI_API_KEY) |
| "Rate limited" | Bot auto-fallbacks to next provider. Add more providers. |
| "Messages not received" | Check Meta dashboard → Webhooks → Recent Deliveries |
| "Bot responds to all group messages" | Ensure `BOT_NAME` matches; users must type `@BotName` |
| "Dashboard not loading data" | Check CORS settings; ensure API URL is correct |

---

## 🚀 Going Live (Meta Business Verification)

For production:

1. **Verify your business** at [business.facebook.com](https://business.facebook.com)
2. **Add a real phone number** to WhatsApp Business
3. **Complete Business Verification** in Meta Business Manager
4. **Submit for review** if needed
5. **Display Name**: Choose a name users will see (e.g., "HaitianBot")

> ⏱️ Business verification takes 1-5 business days.

---

## 🎨 Customizing

### Change Personality
Edit `app/config.py` → `BOT_PERSONALITY` or use dashboard Settings tab.

### Add More AI Providers
Edit `app/services/ai_fallback.py` → add new class inheriting from `AIProvider`.

### Enable/Disable Features
Use dashboard or edit `.env`:
```bash
ENABLE_LONG_TERM_MEMORY=false    # Turn off long-term memory
IMAGE_GENERATION_PROVIDER=none   # Disable image generation
```

---

## 📜 License

MIT License — use it, modify it, sell it. Just don't use it for evil. ✌️

---

**Built with ❤️ for the Haitian community and beyond.**

Questions? Check the troubleshooting section or search your error message online!
