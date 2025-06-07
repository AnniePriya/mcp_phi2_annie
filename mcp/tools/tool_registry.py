
# 4. mcp/tools/tool_registry.py

from .tool import MySQLTool, MongoTool, PDFTool

tool_registry = {
    "mysql": MySQLTool(),
    "mongo": MongoTool(),
    "pdf": PDFTool()
}


