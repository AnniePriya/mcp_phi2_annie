import streamlit as st
from db_connectors.mongo_connector import get_mongo_data
from db_connectors.mysql_connector import get_mysql_data
from utils.pdf_reader import extract_text_from_pdf
from mcp.history_logger import log_history, view_history
from mcp.context_manager import ContextManager
from mcp.mcp_protocol import MCPProtocol
from main import query_openrouter

st.set_page_config(page_title="🧠 MCP Data Agent", layout="wide")

@st.cache_data
def load_data():
    mongo = get_mongo_data("sales1_db", "sales")
    mysql = get_mysql_data("sales_data2")
    pdf = extract_text_from_pdf("pdf_data/ug-mtn-2020-ar-00.PDF")
    return mongo, mysql, pdf

# Load data
with st.spinner("🔄 Loading data..."):
    mongo_data, mysql_data, pdf_data = load_data()

st.title("📊 MCP Personal Data Agent")
st.markdown("""
Welcome to your AI-powered data assistant.  
""")

user_query = st.text_input("Ask your data question..", placeholder="(e.g., 'Which product sold the most in Feb?)")
ask_button = st.button("Ask Now!")

if ask_button and user_query:
    user_id = "12345"
    context = ContextManager()
    context.set_user_id(user_id)
    context.set_active_db("all")
    context.update_db_results("mongo", mongo_data)
    context.update_db_results("mysql", mysql_data)
    context.update_db_results("pdf", pdf_data)

    # Load last 4 history from disk into context memory
    for entry in view_history(user_id)[-4:]:
        context.add_to_history(entry["query"], entry["response"])

    context.update_last_query(user_query)

    # Build prompt with history
    current_prompt = MCPProtocol(context).build_prompt()

    messages = [{"role": "system", "content": "You are a helpful data analyst assistant."}]
    for entry in context.get_history():
        messages.append({"role": "user", "content": entry["query"]})
        messages.append({"role": "assistant", "content": entry["response"]})
    messages.append({"role": "user", "content": current_prompt})

    with st.spinner("🤖 Thinking... Querying DeepSeek via OpenRouter..."):
        result = query_openrouter(messages)

    st.markdown("### ✅ Answer")
    st.success(result)

    # Log & update context
    log_history(user_id, user_query, result)
    context.add_to_history(user_query, result)

# Sidebar for history
st.sidebar.title("📜 Chat History")
history = view_history("12345")

if history:
    for idx, item in enumerate(history[::-1]):
        with st.sidebar.expander(f"🗨️ {item['query'][:30]}...", expanded=(idx == 0)):
            st.markdown(f"**🕒 {item['timestamp']}**")
            st.markdown(f"**Q:** {item['query']}")
            st.markdown(f"**A:** {item['response']}")
else:
    st.sidebar.info("No questions asked yet.")

st.markdown("---\n Made with Keyboard by Annie. Need help? 📧 anniepriya888@gmail.com")
