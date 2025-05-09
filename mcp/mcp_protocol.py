#mcp_protocol.py:
from .context_manager import ContextManager

class MCPProtocol:
    def __init__(self, context: ContextManager):  # Correct constructor
        self.context = context

    def build_prompt(self):                                 
        ctx = self.context.get_context()
        mongo_data = ctx["db_results"].get("mongo", [])
        mysql_data = ctx["db_results"].get("mysql", [])
        user_query = ctx.get("last_query", "")
        active_db = ctx.get("active_db", "both")  # where model chooses the database from the user query

        prompt = (
            "You are a smart data analyst. You will analyze the data provided below "
            "and answer the user's question with specific reasoning.\n\n"
            "Only refer to the data provided below. Use exact product names, months, sales numbers if needed. "
            "Keep it short, accurate, and to the point.\n\n"
        )

        if active_db in ["mongo", "both"]:
            preview_mongo = mongo_data[:2] if isinstance(mongo_data, list) else []
            prompt += f"🔹 MongoDB Data (first 2 rows):\n{preview_mongo}\n\n"

        if active_db in ["mysql", "both"]:
            preview_mysql = mysql_data[:2] if isinstance(mysql_data, list) else []
            prompt += f"🔹 MySQL Data (first 2 rows):\n{preview_mysql}\n\n"

        prompt += (
            f"❓ User Query: {user_query}\n\n"
            "🧠 Analyze based only on the above sample data.\n"
            "👉 Return answer in this format:\n"
            "'<Product Name> in <Month> with amount of $<Amount>, ID: <id>'\n"
            "Give a short reason after the answer. Be precise, don’t guess.\n"
        )

        return prompt.strip()
