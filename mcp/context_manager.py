#context_manager.py:
class ContextManager:
    def __init__(self):  # it should be __init__, not init
        self.context = {
            "user_id": None,
            "last_query": None,
            "db_results": {
                "mongo": [],
                "mysql": []
            },
            "active_db": None
        }

    def set_user_id(self, user_id):
        self.context["user_id"] = user_id

    def update_last_query(self, query):
        self.context["last_query"] = query

    def update_db_results(self, db_name, data):
        if db_name in self.context["db_results"]:
            self.context["db_results"][db_name] = data

    def set_active_db(self, db_name):
        if db_name in ["mongo", "mysql", "both"]:
            self.context["active_db"] = db_name

    def get_context(self):
        return self.context

    def reset_context(self):
        self.__init__()
