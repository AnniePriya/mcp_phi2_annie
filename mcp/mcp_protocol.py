#2. mcp_protocol.py
from .context_manager import ContextManager

class MCPProtocol:
    def __init__(self, context: ContextManager):  
        self.context = context

    def build_prompt(self):                                 
        ctx = self.context.get_context()  # Current memory state from context manager
        
        mongo_data = ctx["db_results"].get("mongo", [])
        mysql_data = ctx["db_results"].get("mysql", [])
        pdf_text = ctx["db_results"].get("pdf", "")
        user_query = ctx.get("last_query", "")
        active_db = ctx.get("active_db", "all")

        prompt = (
            "You are a smart and precise data analyst. Analyze the data provided below.\n"
        )

        if active_db in ["mongo", "all"]:
            preview_mongo = mongo_data[:5] if isinstance(mongo_data, list) else []
            prompt += f"🔹 MongoDB Sample Data:\n{preview_mongo}\n\n"

        if active_db in ["mysql", "all"]:
            preview_mysql = mysql_data[:5] if isinstance(mysql_data, list) else []
            prompt += f"🔹 MySQL Sample Data:\n{preview_mysql}\n\n"
            
        if active_db in ["pdf", "all"]:
            short_pdf = pdf_text.replace('\n', ' ')[:2000]  # limit for safety
            prompt += f"📑 PDF Extract (partial):\n\"{short_pdf}...\"\n\n"

        prompt += (
            f" User Question: {user_query}\n\n"
            " Answer based on the above data.\n"
            " Give a SHORT reason. Be clear and accurate.\n"
        )

        return prompt.strip()
