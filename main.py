# main.py — MCP DeepSeek Chat Agent with History Memory

import os
import requests
from dotenv import load_dotenv
from mcp.context_manager import ContextManager
from mcp.mcp_protocol import MCPProtocol
from mcp.history_logger import log_history, view_history
from mcp.tools.tool_registry import tool_registry
#part 1 of the code - COnnects to the hosted model via openrouter platform
# Load API key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
def query_openrouter(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "MCP-Data-Agent"
    }
    payload = {
        "model": "deepseek/deepseek-chat-v3-0324",
        "max_tokens": 1024,
        "messages": messages
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    try:
        res_json = response.json()                                                                                  #Converts the raw response from OpenRouter into a Python dictionary so you can easily read its parts.
        if "choices" in res_json:                                                                                   #OpenRouter puts the AI’s possible replies, list of answer options.
            return res_json["choices"][0]["message"]["content"]
        else:
            print("❌ OpenRouter Response Error:", res_json)
            return "Something went wrong. Check your API key or model config."
    except Exception as e:
        print("❌ Error while parsing response:", e)
        print("Raw response:", response.text)
        return "Failed to get a valid response."

# ======MAIN =====
if __name__ == "__main__":
    print("\n🖥️ FETCHING DATA FROM MONGODB, MYSQL, and PDF ...")

    params_map = {
        "mongo": {"db_name": "sales1_db", "collection_name": "sales"},
        "mysql": {"table_name": "sales_data2"},
        "pdf": {"pdf_path": "pdf_data/ug-mtn-2020-ar-00.PDF"}
    }

    try:
        mongo_data = tool_registry["mongo"].run(**params_map["mongo"])
        print("✅ MongoDB Data fetched.")
    except Exception as e:
        print("⚠️ Failed to fetch Mongo data:", e)
        mongo_data = []

    try:
        mysql_data = tool_registry["mysql"].run(**params_map["mysql"])               #actual MySQL tool object ready to fetch MySQL data when you call .run() on it.
        print("✅ MySQL Data fetched.")
    except Exception as e:
        print("⚠️ Failed to fetch MySQL data:", e)
        mysql_data = []

    try:
        pdf_text = tool_registry["pdf"].run(**params_map["pdf"])
        print("📑 PDF Data loaded.")
    except Exception as e:
        print("⚠️ Failed to load PDF:", e)
        pdf_text = ""

    #  Context ssetup 
    context = ContextManager()
    user_id = "12345"
    context.set_user_id(user_id)
    context.set_active_db("all")
    context.update_db_results("mongo", mongo_data)
    context.update_db_results("mysql", mysql_data)
    context.update_db_results("pdf", pdf_text)

    # Loaded last 4 history entries from file into memory 
    for entry in view_history(user_id)[-4:]:
        context.add_to_history(entry["query"], entry["response"])

    
    print("\n💬 Ask your data question (e.g., 'Which product sold the most in Feb?'):")
    user_query = input("👉 ")

    context.update_last_query(user_query)
#looped over history and added both user + assistant messages
    # conversation context
    current_prompt = MCPProtocol(context).build_prompt()

    messages = [{"role": "system", "content": "You are a helpful data analyst assistant."}]
    for entry in context.get_history():
        messages.append({"role": "user", "content": entry["query"]})
        messages.append({"role": "assistant", "content": entry["response"]})
    messages.append({"role": "user", "content": current_prompt})

    #Calling model
    print("\n⏳ Querying DeepSeek V3 via OpenRouter...\n")
    result = query_openrouter(messages)
    print("🤖 Response:\n", result)

    # Log interaction to memory json with the history_logger
    log_history(user_id, user_query, result)
    context.add_to_history(user_query, result)
    
