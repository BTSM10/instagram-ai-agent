# Automation & AI Tools

A collection of automation projects built with Python, n8n, LangChain, and cloud APIs.

---

## Projects

### 1. Instagram AI Digest Agent
**`instagram_ai_agent/`**

An autonomous agent that monitors Instagram accounts of AI creators, summarizes their posts using an LLM, and delivers a daily educational digest by email — with no manual intervention.

**How it works:**
1. Scrapes posts from target Instagram accounts via the Apify cloud scraping API
2. Summarizes content using LangChain + Groq (LLaMA 3.3 70B) with a structured prompt that defines every tool, model, and concept mentioned
3. Sends a formatted HTML email digest via Gmail SMTP
4. Runs daily on a GitHub Actions cron schedule (no laptop required)

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

### 2. Instagram AI Digest — n8n Workflow
**`instagram_ai_agent/n8n_workflow.json`**

The same pipeline rebuilt as a visual no-code workflow in n8n — importable in one click.

**Pipeline:**
```
Schedule Trigger → Start Apify Run → Wait 45s → Fetch Dataset → Format Posts → Groq Summarize → Send Email
```

**Key engineering notes:**
- The **Format Posts** Code node runs `runOnceForAllItems` to collapse multiple scraped posts into a single LLM prompt, and uses `JSON.stringify()` to safely serialize post captions (which may contain quotes and newlines) into the Groq request body
- The **Wait 45s** node gives Apify time to finish scraping before the dataset is fetched — removing it returns an empty dataset
- Email is sent via SMTP credentials (no Google OAuth app required)

**Import into n8n:**
1. Open n8n → New Workflow → `...` menu → Import from JSON
2. Paste contents of `n8n_workflow.json`
3. Add your Apify token, Groq API key, and SMTP credentials
4. Click Test workflow

**Stack:** n8n · Docker · Apify API · Groq API · SMTP

---

### 3. File Organizer
**`file_organizer.py`**

Automatically sorts files in a folder into subfolders by type.

```bash
python3 file_organizer.py              # organizes ~/Downloads
python3 file_organizer.py ~/Desktop   # organizes any folder
```

| Folder | File Types |
|---|---|
| Images | .jpg, .jpeg, .png, .gif, .webp |
| Documents | .pdf, .docx, .txt, .xlsx, .html |
| Videos | .mp4, .mov, .avi, .mkv |
| Audio | .mp3, .wav, .aac, .flac |
| Archives | .zip, .tar, .gz, .rar |
| Code | .py, .js, .ts, .css, .json |

---

### 4. File Finder
**`find_file.py`**

Searches your Mac for a file by name and opens it in Finder.

```bash
# Add alias for convenience
echo 'alias findfile="python3 ~/Desktop/P/find_file.py"' >> ~/.zshrc
source ~/.zshrc

findfile report          # partial match
findfile Biniam Tsige CV # spaces supported
```

---

## Requirements

- Python 3.10+
- Docker (for n8n local setup)
- API keys: Groq (free), Apify (free tier), Gmail App Password
