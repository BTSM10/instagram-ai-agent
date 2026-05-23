import os
from datetime import datetime, timezone, timedelta
from typing import Optional
from apify_client import ApifyClient


def get_recent_posts(accounts: list[str], lookback_hours: int = 24,
                     instagram_user: Optional[str] = None,
                     instagram_pass: Optional[str] = None) -> list[dict]:
    """
    Fetches posts from the last `lookback_hours` for each account using Apify.
    """
    apify_token = os.getenv("APIFY_API_TOKEN")
    if not apify_token:
        print("[scraper] ERROR: APIFY_API_TOKEN not set in .env.")
        return []

    client = ApifyClient(apify_token)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
    collected = []

    for username in accounts:
        print(f"[scraper] Fetching posts from @{username} via Apify ...")
        try:
            run = client.actor("apify/instagram-profile-scraper").call(
                run_input={
                    "usernames": [username],
                    "resultsLimit": 20,
                }
            )
            dataset_id = (
                run["defaultDatasetId"] if isinstance(run, dict)
                else run.default_dataset_id
            )
            for profile in client.dataset(dataset_id).iterate_items():
                for post in profile.get("latestPosts") or []:
                    ts_str = post.get("timestamp") or ""
                    if ts_str:
                        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        if ts < cutoff:
                            continue
                    else:
                        ts = None

                    caption = (post.get("caption") or "").strip()
                    if not caption:
                        continue

                    short_code = post.get("shortCode") or ""
                    url = post.get("url") or (
                        f"https://www.instagram.com/p/{short_code}/" if short_code else ""
                    )

                    collected.append({
                        "username": username,
                        "timestamp": ts.strftime("%Y-%m-%d %H:%M UTC") if ts else "Unknown",
                        "caption": caption[:2000],
                        "url": url,
                        "likes": post.get("likesCount", 0),
                        "post_type": (post.get("type") or "image").lower(),
                    })
        except Exception as e:
            print(f"[scraper] Error fetching @{username}: {e}")

    print(f"[scraper] Collected {len(collected)} post(s) total.")
    return collected
