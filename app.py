import streamlit as st
from db_connectors.mongo_connector import get_mongo_data
from db_connectors.mysql_connector import get_mysql_data
from utils.pdf_reader import extract_text_from_pdf
from mcp.history_logger import log_history, view_history
from main import query_openrouter

# Streamlit Page Config
st.set_page_config(page_title="🧠 MCP Data Agent", layout="wide")

# Load data on startup
@st.cache_data
def load_data():
    mongo = get_mongo_data("sales1_db", "sales")
    mysql = get_mysql_data("sales_data2")
    pdf = extract_text_from_pdf("pdf_data/ug-mtn-2020-ar-00.PDF")
    return mongo, mysql, pdf

# Sidebar
st.sidebar.title("⚙️ Settings")
active_db = st.sidebar.radio("Select Data Source", ["all", "mongo", "mysql", "pdf"], index=0)


with st.spinner("🔄 Loading data from all sources..."):
    mongo_data, mysql_data, pdf_data = load_data()

# Title and Instructions
st.title("📊 MCP Personal Data Agent")
st.markdown("""
Welcome to your AI-powered data assistant.\n
💡 Ask questions and get answers based on:

""")


with st.container():
    user_query = st.text_input("💬 Ask your question here:", placeholder="e.g., List all the products from the data")
    ask_button = st.button("🚀 Ask Now")

# Response logic
if ask_button and user_query:
    # Build prompt like in main.py
    formatted_prompt = f"""
I am providing you with two sets of data from two databases and a pdf.

🔹 MongoDB data:
{mongo_data[:10]}  

🔹 MySQL data:
{mysql_data[:10]}  

🔹 PDF data:
{pdf_data}  

Now based on this information, please answer the following question:

❓ {user_query}
"""

    with st.spinner("🤖 Thinking... Querying DeepSeek via OpenRouter..."):
        result = query_openrouter(formatted_prompt)

    st.markdown("### ✅ Answer")
    st.success(result)
    log_history("12345", user_query, result)

# History viewer
st.sidebar.markdown("---")
if st.sidebar.button("📜 View Past Queries"):
    st.sidebar.subheader("Query History")
    history = view_history("12345")
    for item in history[::-1]:
        st.sidebar.markdown(f"**Q:** {item['query']}\n\n**A:** {item['response']}")

# Footer note
st.markdown("""
---
Made with Keyboard by Annie. 
Need help? anniepriya888@gmail.com😉
""")