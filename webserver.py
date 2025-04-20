from flask import Flask, request, render_template
import sqlite3
import os
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
import google.generativeai as genai

app = Flask(__name__)

# Initialize SQLite database
db_name = "local_database.db"

# Pinecone and Gemini Configuration
pc = Pinecone(
    api_key=""  # Replace with your Pinecone API key
)
index_name = "formulae-index"  # Ensure this matches the trained index
index = pc.Index(index_name)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")
API_KEY = "AIzaSyAZsRTDVpsPRhHpezqaIc2ZvanreBv0Xx4"
genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Helper Functions
def execute_sql(sql_query):
    """Execute SQL queries and return results"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        # For SELECT queries, execute and get column names
        if sql_query.strip().upper().startswith("SELECT"):
            cursor.execute(sql_query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            return {"columns": columns, "rows": rows}, None
        # For non-SELECT queries
        cursor.executescript(sql_query)
        conn.commit()
        return None, "Query executed successfully."
    except sqlite3.Error as e:
        return None, f"Error: {str(e)}"
    finally:
        conn.close()

def get_table_names():
    """Get all table names from database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def get_database_structure():
    """Retrieve the structure of all tables in the database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    structure = []
    try:
        tables = get_table_names()
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            structure.append({"table": table, "columns": columns})
    finally:
        conn.close()
    return structure

def format_database_structure(structure):
    """Format the database structure for inclusion in prompts"""
    formatted = ""
    for table_info in structure:
        formatted += f"Table: {table_info['table']}\n"
        for column in table_info['columns']:
            formatted += f"  - {column[1]} ({column[2]})\n"
    return formatted

def query_gemini(natural_query, relevant_info):
    """Use Google Gemini to generate SQL queries"""
    try:
        chat = gemini_model.start_chat()
        database_structure = format_database_structure(get_database_structure())
        prompt = f"""
        You are an AI system answering queries based on a data store. 
        Here is the data you should use:
        {relevant_info}

        Here is the latest database structure:
        {database_structure}

        Here is the user's query:
        {natural_query}

        You are supposed to take this data into context and write SQL queries if asked to do so. 
        If not asked to write SQL queries, then reply in natural language. 
        If there is any SQL code in your response, simply reply with only and only the SQL code and absolutely nothing else, no other text.
        Also, when writing sql code, dont encapsulate it within the ```sql   ``` quotes, simply reply with the text of the sql code
        """
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"Error querying Gemini: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    message = None
    natural_query = request.form.get("natural_query", "")
    suggested_query = request.form.get("suggested_query", "")
    table_data = None
    table_columns = None
    selected_table = None

    if request.method == "POST":
        if "natural_query" in request.form and natural_query:
            # Generate SQL query using Gemini
            query_embedding = embeddings.embed_query(natural_query)
            response = index.query(vector=query_embedding, top_k=4, include_metadata=True)
            if response.matches:
                relevant_info = "\n".join([match["metadata"]["content"] for match in response.matches])
                suggested_query = query_gemini(natural_query, relevant_info)

        elif "execute_query" in request.form:
            suggested_query = request.form.get("suggested_query")
            if suggested_query:
                result, message = execute_sql(suggested_query)

        elif "table_name" in request.form:
            selected_table = request.form.get("table_name")
            if selected_table:
                table_result, _ = execute_sql(f"SELECT * FROM {selected_table}")
                if table_result:
                    table_columns = table_result["columns"]
                    table_data = table_result["rows"]

    tables = get_table_names()
    return render_template(
        "index.html",
        tables=tables,
        result=result,
        message=message,
        suggested_query=suggested_query,
        table_data=table_data,
        table_columns=table_columns,
        natural_query=natural_query,
        selected_table=selected_table,
    )

if __name__ == "__main__":
    app.run(debug=True)
