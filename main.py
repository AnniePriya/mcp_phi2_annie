#main.py:
from db_connectors.mongo_connector import get_mongo_data
from db_connectors.mysql_connector import get_mysql_data
from mcp.context_manager import ContextManager
from mcp.mcp_protocol import MCPProtocol
from mcp.history_logger import log_history, view_history
import subprocess

def query_phi(prompt):
    ollama_path = r"C:\Users\HP\AppData\Local\Programs\Ollama\ollama.exe"
    process = subprocess.Popen(
        [ollama_path, 'run', 'phi'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    stdout, stderr = process.communicate(prompt)
    return stdout.strip()

if __name__ == "__main__":  # ✅ Corrected this line
    print("\n 🖥️ FETCHING THE DATA FROM THE DATABASES.... \n")

    # Get data from both sources
    mongo_data = get_mongo_data("sales1_db", "sales")
    mysql_data = get_mysql_data("sales2")

    print(" 🏳️ Mongo Data fetched.")
    print(" 🏳️ MySQL Data fetched.")

    # Setup context
    context = ContextManager()
    context.set_user_id("12345")
    context.update_db_results("mongo", mongo_data)
    context.update_db_results("mysql", mysql_data)

    # Accept user query
    user_query = input("\n ❓ Ask a question about the data: ")
    context.update_last_query(user_query)

    # 🧠 Auto-detect DB from user query
    lowered = user_query.lower()
    if "mysql" in lowered:
        context.set_active_db("mysql")
    elif "mongo" in lowered:
        context.set_active_db("mongo")
    else:
        context.set_active_db("both")

    
    if "compare" in lowered:
        print("🔍 Compare requested — model will offer separate or unified output!")

    # Build and send prompt to Phi
    mcp = MCPProtocol(context)
    formatted_prompt = mcp.build_prompt()

    print("\n Querying phi..\n")
    result = query_phi(formatted_prompt)
    print("\n 🤖 phi says:🤖 \n", result)

    # Save to history
    log_history("12345", user_query, result)
