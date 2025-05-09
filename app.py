from flask import Flask, render_template, request
from mcp.context_manager import ContextManager
from mcp.mcp_protocol import MCPProtocol
from db_connectors.mongo_connector import get_mongo_data
from db_connectors.mysql_connector import get_mysql_data
import subprocess

app = Flask(__name__)

# Load data once when the server starts
mongo_data = get_mongo_data("sales1_db", "sales")
mysql_data = get_mysql_data("sales2")

context = ContextManager()
context.set_user_id("12345")
context.update_db_results("mongo", mongo_data)
context.update_db_results("mysql", mysql_data)

def query_phi(prompt):
    ollama_path = r"C:\\Users\\HP\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
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

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        user_query = request.form["query"]
        context.update_last_query(user_query)

        # Choose DB based on query
        lowered = user_query.lower()
        if "mysql" in lowered:
            context.set_active_db("mysql")
        elif "mongo" in lowered:
            context.set_active_db("mongo")
        else:
            context.set_active_db("both")

        # Build prompt & query phi
        mcp = MCPProtocol(context)
        formatted_prompt = mcp.build_prompt()
        response = query_phi(formatted_prompt)

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
