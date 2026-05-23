#!/usr/bin/env python3
"""
Instagram AI Digest Agent
Runs on a daily schedule: scrapes → summarizes → emails.

Usage:
  python main.py           # starts the scheduler (runs every day at send_time)
  python main.py --now     # run immediately once (great for testing)
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime

import schedule
from dotenv import load_dotenv

from scraper import get_recent_posts
from summarizer import generate_digest
from emailer import send_digest


def load_config(path: str = "config.json") -> dict:
    with open(path) as f:
        return json.load(f)


def run_pipeline(config: dict) -> None:
    print(f"\n{'='*50}")
    print(f"[agent] Starting pipeline at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    # --- Credentials from environment ---
    groq_key = os.getenv("GROQ_API_KEY")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    apify_token = os.getenv("APIFY_API_TOKEN")

    if not groq_key:
        print("[agent] ERROR: GROQ_API_KEY not set in .env. Aborting.")
        return
    if not gmail_password:
        print("[agent] ERROR: GMAIL_APP_PASSWORD not set in .env. Aborting.")
        return
    if not apify_token:
        print("[agent] ERROR: APIFY_API_TOKEN not set in .env. Aborting.")
        return

    os.environ["GROQ_API_KEY"] = groq_key  # LangChain reads this automatically

    # --- 1. Scrape ---
    posts = get_recent_posts(
        accounts=config["instagram_accounts"],
        lookback_hours=config.get("lookback_hours", 24),
    )

    # --- 2. Summarize ---
    date_str = datetime.now().strftime("%A, %B %d %Y")
    digest = generate_digest(
        posts=posts,
        model=config["groq"]["model"],
        date_str=date_str,
    )
    print("\n--- DIGEST PREVIEW ---")
    print(digest[:500], "...\n" if len(digest) > 500 else "\n")

    # --- 3. Email ---
    send_digest(digest, config, gmail_password)

    print("[agent] Pipeline complete.")


def main():
    load_dotenv()  # loads .env from current directory

    parser = argparse.ArgumentParser(description="Instagram AI Digest Agent")
    parser.add_argument("--now", action="store_true",
                        help="Run the pipeline immediately instead of waiting for schedule")
    parser.add_argument("--config", default="config.json",
                        help="Path to config file (default: config.json)")
    args = parser.parse_args()

    config = load_config(args.config)
    send_time = config["schedule"]["send_time"]  # e.g. "08:00"

    if args.now:
        run_pipeline(config)
        return

    print(f"[agent] Scheduler started. Will run daily at {send_time}.")
    print("[agent] Press Ctrl+C to stop.\n")

    schedule.every().day.at(send_time).do(run_pipeline, config=config)

    # Run once immediately on startup so you can verify it works
    run_pipeline(config)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
