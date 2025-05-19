# history_logger.py:
import json
import os
from datetime import datetime

HISTORY_FILE = "mcp/history_log.json"

def log_history(user_id, query, response, filepath="mcp/history_log.json"):
    new_entry = {
        "user_id": user_id,
        "query": query,
        "response": response,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(new_entry)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def view_history(user_id=None):
    if not os.path.exists(HISTORY_FILE):
        print("No history found.")
        return

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    print("\n📜 History Log:\n")
    for entry in history:
        if user_id and entry["user_id"] != user_id:
            continue
        print(f"🕒 {entry['timestamp']}")
        print(f"❓ Q: {entry['query']}")
        print(f"🤖 A: {entry['response']}\n")
