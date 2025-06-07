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

#view histroy  loads all the things

def view_history(user_id=None):
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []

    # Return only relevant entries
    if user_id:
        return [entry for entry in history if entry["user_id"] == user_id]
    return history

