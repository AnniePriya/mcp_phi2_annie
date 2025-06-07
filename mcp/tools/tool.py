# 5. mcp/tool.py

class Tool:
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func

    def run(self, **kwargs):
        return self.func(**kwargs)
    
from db_connectors.mysql_connector import get_mysql_data                                  # Tool classes wrapping your current data fetchers
from db_connectors.mongo_connector import get_mongo_data
from utils.pdf_reader import extract_text_from_pdf
#MySQLTool `1`
class MySQLTool(Tool):
    def __init__(self):
        super().__init__(
            name="mysql",
            description="Fetch data from MySQL",
            func=get_mysql_data
        )
#MongoTool `2`
class MongoTool(Tool):
    def __init__(self):
        super().__init__(
            name="mongo",
            description="Fetch data from MongoDB",
            func=get_mongo_data
        )
#PDFTool `3`
class PDFTool(Tool):
    def __init__(self):
        super().__init__(
            name="pdf",
            description="Extract text from PDF",
            func=extract_text_from_pdf
        )