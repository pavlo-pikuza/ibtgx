import os
import time
import requests
import asyncio
from dotenv import load_dotenv

from ib.account import get_accounts, get_account_balance
from ib.portfolio import get_portfolio

load_dotenv()

TG_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_ALLOWED_CHATS = list(map(int, os.getenv("TG_ALLOWED_CHATS", "").split(',')))
TG_API_URL = f"https://api.telegram.org/bot{TG_TOKEN}/"

def send_text(chat_id, text):
    requests.post(TG_API_URL + "sendMessage", data={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    })

def listen_for_commands():
    last_update_id = None
    while True:
        try:
            resp = requests.get(TG_API_URL + "getUpdates", params={"timeout": 60, "offset": last_update_id}, timeout=90)
            data = resp.json()

            for update in data.get("result", []):
                last_update_id = update["update_id"] + 1
                msg = update.get("message", {})
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id")

                if chat_id not in TG_ALLOWED_CHATS:
                    continue

                if text == "/accounts":
                    reply = asyncio.run(get_accounts())
                    send_text(chat_id, reply)

                #if text == "/balance":
                #    reply = asyncio.run(get_account_balance())
                #    send_text(chat_id, reply)

                elif text == "/portfolio":
                    reply = asyncio.run(get_portfolio())
                    send_text(chat_id, reply)

        except Exception as e:
            print(f"[TG Listener error] {e}")
            time.sleep(10)