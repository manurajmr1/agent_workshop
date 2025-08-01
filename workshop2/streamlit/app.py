import streamlit as st
import requests
import mysql.connector
import os

LLAMA_API_URL = os.environ.get("LLAMA_API_URL", "http://localhost:8000")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "salesuser")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "salespass")
MYSQL_DB = os.environ.get("MYSQL_DB", "salesdb")

# Prompt template for LLM to generate SQL
PROMPT_TEMPLATE = '''
You are an expert MySQL assistant for a sales order database. The schema is:

Table users(id, name, email)
Table orders(id, user_id, product, amount, order_date)

Given a user question, generate only the corresponding syntactically correct MySQL query as the response. Do not include any explanation, comments, or extra text. Only output the SQL query.

Question: {question}
'''

def ask_llama(question):
    prompt = PROMPT_TEMPLATE.format(question=question)
    # Ollama expects /api/generate and a JSON with 'model' and 'prompt'
    response = requests.post(
        f"{LLAMA_API_URL}/api/generate",
        json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }
    )
    # Ollama returns {'response': ...}
    return response.json().get("response", "")

def run_query(sql):
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
        else:
            conn.commit()
            return [], []
    except Exception as e:
        return [], [[f"Error: {e}"]]
    finally:
        cursor.close()
        conn.close()

def extract_sql(text):
    # Find the first line that looks like SQL and return from there
    sql_keywords = ("SELECT", "INSERT", "UPDATE", "DELETE")
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if any(line.strip().upper().startswith(k) for k in sql_keywords):
            return "\n".join(lines[i:]).strip()
    return text.strip()

# Add sidebar with sample questions
st.sidebar.title("Sample Questions")
sample_questions = [
    "Show all orders",
    "List users who bought a Laptop",
    "What is the total sales amount?",
    "Show all orders placed by Alice",
    "Get order amount for a specific product"
]
if 'sample_selected' not in st.session_state:
    st.session_state['sample_selected'] = ''
for q in sample_questions:
    if st.sidebar.button(q, key=q):
        st.session_state['sample_selected'] = q
        st.session_state['chat_input'] = q  # Set the text input value

# Main title
st.title("AI Sales Order Chatbot")

if "history" not in st.session_state:
    st.session_state["history"] = []

# Use the sample if selected, else keep user input
user_input = st.text_input(
    "Ask about sales orders, users, etc:",
    value=st.session_state.get('chat_input', ''),
    key="chat_input"
)

send_clicked = st.button("Send")

if send_clicked and user_input:
    with st.spinner("Thinking..."):
        raw_sql = ask_llama(user_input)
        sql = extract_sql(raw_sql)
        sql = sql.split(';')[0].strip() + ';' if ';' in sql else sql.strip()
        columns, rows = run_query(sql)
        new_block = [
            ("user", user_input),
            ("llama", sql),
            ("db_table", (columns, rows)) if columns else ("db", rows[0][0] if rows else "No results.")
        ]
        st.session_state["history"] = new_block + st.session_state["history"]

# Show chat history in order (newest at top, oldest at bottom)
st.markdown("---")
st.markdown("### Chat History")
for sender, msg in st.session_state["history"]:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    elif sender == "llama":
        st.markdown(f"**Llama (SQL):**")
        st.code(msg, language="sql")
    elif sender == "db_table":
        columns, rows = msg
        st.markdown("**DB Results:**")
        st.dataframe({col: [row[i] for row in rows] for i, col in enumerate(columns)})
    elif sender == "db":
        st.markdown(f"**DB:** {msg}")
