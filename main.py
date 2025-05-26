#main.py_open router // -- deepseek 
import os
import requests
from dotenv import load_dotenv
from db_connectors.mongo_connector import get_mongo_data
from db_connectors.mysql_connector import get_mysql_data
from mcp.context_manager import ContextManager
from mcp.mcp_protocol import MCPProtocol
from mcp.history_logger import log_history, view_history
from utils.pdf_reader import extract_text_from_pdf  


load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") 

# via opren router connect
def query_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",  
        "X-Title": "MCP-Data-Agent"
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324",
        "max_tokens": 1024,  
        "messages": [
            {"role": "system", "content": "You are a helpful data analyst assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    try:
        res_json = response.json()
        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        else:
            print("❌ OpenRouter Response Error:")
            print(res_json)
            return "Something went wrong. Check your API key, quota, or model name."
    except Exception as e:
        print("❌ Exception while parsing response:", e)
        print("Response content:", response.text)
        return "Failed to get response."


# MAIN PROGRAM
if __name__ == "__main__":
    print("\n  🖥️  FETCHING DATA FROM MONGODB,MYSQL and PDF ...")

    # Fetch MongoDB data
    try:
        mongo_data = get_mongo_data("sales1_db", "sales")
        print("✅ MongoDB Data fetched.")
    except Exception as e:
        print("⚠️ Failed to fetch Mongo data:", e)
        mongo_data = {}

    
    try:
        mysql_data = get_mysql_data("sales_data2")
        print("✅ MySQL Data fetched.")
    except Exception as e:
        print("⚠️ Failed to fetch MySQL data:", e)
        mysql_data = {}

     
    pdf_text = ""
    pdf_path = "pdf_data/ug-mtn-2020-ar-00.PDF"  
    if os.path.exists(pdf_path):
        pdf_text = extract_text_from_pdf(pdf_path)
        print("📑 PDF Data loaded.")
    else:
        print("⚠️ PDF file not found.")

    
    print("\n💬 Ask your data question (like 'List all the products from the data'): ")
    user_query = input("👉 ")

    
    formatted_prompt = f"""
I am providing you with two sets of data from two databases and a pdf.

🔹 MongoDB data:
{mongo_data[:10]}  

🔹 MySQL data:
{mysql_data[:10]}  

🔹 PDF data:
{pdf_text}  

Now based on this information, please answer the following question:

❓ {user_query}
"""

    print("\n⏳ Querying DeepSeek: DeepSeek V3 0324 via OpenRouter...\n")
    result = query_openrouter(formatted_prompt)

    print("🤖 Response:\n", result)

    log_history("12345", user_query, result)
