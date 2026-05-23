#!/usr/bin/env python3
"""
Run this once to create an Instagram session from your Chrome browser cookies.
Make sure you are logged into Instagram in Chrome (Default profile) before running.

Usage:
    python3 setup_session.py
"""
import sys
import os
import shutil
import tempfile
import browser_cookie3
import instaloader
from dotenv import load_dotenv

CHROME_COOKIE_FILE = os.path.expanduser(
    "~/Library/Application Support/Google/Chrome/Default/Cookies"
)


def get_username():
    load_dotenv()
    return os.getenv("INSTAGRAM_USERNAME", "").lower()


def main():
    username = get_username()
    if not username:
        username = input("Enter your Instagram username: ").strip().lower()

    print(f"[setup] Reading Instagram cookies from Chrome Default profile...")

    # browser_cookie3 locks the file while Chrome is open, so we copy it first
    tmp = tempfile.mktemp(suffix=".db")
    shutil.copy2(CHROME_COOKIE_FILE, tmp)

    try:
        cookie_jar = browser_cookie3.chrome(
            cookie_file=tmp,
            domain_name=".instagram.com"
        )
    except Exception as e:
        print(f"[setup] Could not read Chrome cookies: {e}")
        sys.exit(1)
    finally:
        os.unlink(tmp)

    cookies = {c.name: c.value for c in cookie_jar}
    if "sessionid" not in cookies:
        print("[setup] No Instagram login found in Chrome Default profile.")
        print("[setup] Open Chrome, go to instagram.com, log in, then run this again.")
        sys.exit(1)

    print(f"[setup] Instagram session found. Saving for @{username} ...")

    loader = instaloader.Instaloader(quiet=True)
    for cookie in cookie_jar:
        loader.context._session.cookies.set(
            cookie.name, cookie.value, domain=cookie.domain
        )
    loader.context.username = username

    loader.save_session_to_file(username)
    print(f"[setup] Done! Session saved.")
    print(f"[setup] Now run:  python3 main.py --now")


if __name__ == "__main__":
    main()
