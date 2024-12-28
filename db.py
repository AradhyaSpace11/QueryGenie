from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

# Initialize SQLite database
db_name = "local_database.db"

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

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    message = None
    table_data = None
    selected_table = None

    if request.method == "POST":
        if "sql_query" in request.form:
            sql_query = request.form.get("sql_query")
            if sql_query:
                result, message = execute_sql(sql_query)
        
        if "table_name" in request.form:
            selected_table = request.form.get("table_name")
            if selected_table:
                table_data, _ = execute_sql(f"SELECT * FROM {selected_table}")

    tables = get_table_names()
    
    return render_template(
        "index.html",
        tables=tables,
        result=result,
        message=message,
        table_data=table_data,
        selected_table=selected_table
    )

if __name__ == "__main__":
    app.run(debug=True)