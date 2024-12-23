# QueryGenie

**QueryGenie** is an AI-powered SQL query generator that uses Retrieval-Augmented Generation (RAG) to dynamically create SQL queries based on user prompts and a stored knowledge base. It’s designed to bridge the gap between complex data and simple language, helping users efficiently interact with databases without needing to be SQL experts.

## 📖 Overview

QueryGenie leverages the RAG framework, where relevant information is pulled from a knowledge base to provide context and accuracy for SQL query generation. With QueryGenie, users can generate precise queries that adapt to complex data structures, making it especially useful for database management, data analysis, and automated reporting.

## 🔍 Features

- **Natural Language to SQL**: Converts human language input into SQL queries.
- **Knowledge Store Integration**: Retrieves relevant information from the knowledge base to enhance SQL query accuracy.
- **Customizable**: Adaptable to various database schemas by updating the knowledge store.
- **Optimized for Accuracy**: Uses retrieval to ensure the SQL query aligns with available data and user intent.

## ⚙️ How It Works

1. **User Input**: The user provides a prompt (e.g., “Show me all sales in Q1 of 2023”).
2. **Retrieve Context**: QueryGenie searches the knowledge base for relevant information related to the prompt.
3. **Generate SQL**: Using RAG, the system formulates an SQL query based on the retrieved information and user input.
4. **Query Output**: The generated SQL query is displayed or executed against the connected database.

## 🤖 Example

**Input**:
> "List all customers who made a purchase in January 2023"

**Generated SQL**:
```sql
SELECT * FROM customers
WHERE purchase_date BETWEEN '2023-01-01' AND '2023-01-31';




