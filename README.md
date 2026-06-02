# Instagram AI Digest Agent

An autonomous agent that monitors Instagram accounts of AI creators, summarizes their posts using an LLM, and delivers a daily educational digest by email — with no manual intervention.

---

## How it works

1. Scrapes posts from target Instagram accounts via the Apify cloud scraping API
2. Summarizes content using LangChain + Groq (LLaMA 3.3 70B) with a structured prompt that defines every tool, model, and concept mentioned
3. Sends a formatted HTML email digest via Gmail SMTP
4. Runs daily on a GitHub Actions cron schedule — no laptop required

---

## Projects

### Python Agent
**`instagram_ai_agent/`**

**Stack:** Python · LangChain · Groq API · Apify · GitHub Actions · smtplib

**Setup:**
```bash
cd instagram_ai_agent
pip install -r requirements.txt
cp .env.example .env   # add GROQ_API_KEY, GMAIL_APP_PASSWORD, APIFY_API_TOKEN
python main.py --now   # run immediately
```

**Config** (`config.json`):
```json
{
  "instagram_accounts": ["mattmurphyai", "kernx.ai", "sayed.developer"],
  "lookback_hours": 24,
  "email": { "from": "you@gmail.com", "to": "you@gmail.com" }
}
```

**Cloud deployment:** Secrets are stored in GitHub Actions (never committed). The workflow runs at 05:00 UTC (08:00 EAT) daily via `.github/workflows/instagram-digest.yml`.

---

### n8n Workflow
**`instagram_ai_agent/n8n_workflow.json`**

The same pipeline rebuilt as a visual no-code workflow in n8n — importable in one click.

**Pipeline:**
```
Schedule Trigger → Start Apify Run → Wait 45s → Fetch Dataset → Format Posts → Groq Summarize → Send Email
```

**Import into n8n:**
1. Open n8n → New Workflow → `...` menu → Import from JSON
2. Paste contents of `n8n_workflow.json`
3. Add your Apify token, Groq API key, and SMTP credentials
4. Click Test workflow

**Stack:** n8n · Docker · Apify API · Groq API · SMTP

---

## Requirements

- Python 3.10+
- Docker (for n8n local setup)
- API keys: Groq (free), Apify (free tier), Gmail App Password
