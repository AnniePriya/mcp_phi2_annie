#mcp_protocol.py:
from .context_manager import ContextManager

class MCPProtocol:
    def __init__(self, context: ContextManager):  
        self.context = context

    def build_prompt(self):                                 
        ctx = self.context.get_context()   #current state of mem from context manager
        mongo_data = ctx["db_results"].get("mongo", [])
        mysql_data = ctx["db_results"].get("mysql", [])
        user_query = ctx.get("last_query", "")
        pdf_text = ctx["db_results"].get("pdf", "")
        active_db = ctx.get("active_db", "all")  # where model chooses the database from the user query

        prompt = (
            "You are a smart data analyst. You will analyze the data provided below "
            "and answer the user's question with specific reasoning.\n\n"
             "You are a precise and careful data analyst. Only use the data provided below.\n"
             "If the answer is not found, say 'Data not available.' Do not guess.\n\n"
            "Only refer to the data provided below. Use exact product names, months, sales numbers if needed. "
            "Keep it short, accurate, and to the point.\n\n"
        )

        if active_db in ["mongo", "all"]:
            preview_mongo = mongo_data[:5] if isinstance(mongo_data, list) else []
            prompt += f"🔹 MongoDB Data (first 5 rows):\n{preview_mongo}\n\n"

        if active_db in ["mysql", "all"]:
            preview_mysql = mysql_data[:5] if isinstance(mysql_data, list) else []
            prompt += f"🔹 MySQL Data (first 5 rows):\n{preview_mysql}\n\n"
            
        if active_db in ["pdf", "all"]:
            short_pdf = pdf_text.replace('\n', ' ')  
            prompt += f"📑 PDF Extract (partial text):\n\"{short_pdf}...\"\n\n"

        prompt += (
            f"❓ User Query: {user_query}\n\n"
            "🧠 Analyze based only on the above sample data.\n"
            "👉 Return answer in this format:\n"
            "'<Product Name> in <Month> with amount of $<Amount>, ID: <id>'\n"
            "Give a short reason after the answer. Be precise, don’t guess.\n"
        )

        return prompt.strip()
