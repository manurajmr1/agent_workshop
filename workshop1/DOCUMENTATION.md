# AI Sales Order Chatbot - Application Documentation

## Overview

This application is a **Natural Language to SQL AI Agent** built with Streamlit that allows users to query a sales database using natural language. It leverages a local LLM (LLaMA 3.2:1b) via Ollama to translate user questions into SQL queries and execute them against a MySQL database.

## Architecture Type

**Classification**: AI Agent (Text-to-SQL Agent)

This is not a simple LLM API implementation, but rather an **intelligent agent** that:
- Accepts natural language queries
- Uses an LLM to translate them to SQL
- Executes the SQL against a database
- Returns formatted results to the user
- Maintains conversation history

## System Architecture

```
User Input (Natural Language)
        ↓
    Streamlit UI
        ↓
    LLaMA 3.2:1b (via Ollama)
        ↓
    SQL Query Generation
        ↓
    MySQL Database Execution
        ↓
    Formatted Results Display
```

## Components

### 1. **Frontend Layer** (`app.py`)
- **Framework**: Streamlit
- **Purpose**: Web-based user interface for natural language queries
- **Features**:
  - Chat-like interface
  - Sample question buttons
  - SQL query display
  - Tabular result presentation
  - Conversation history

### 2. **AI Layer** (LLaMA via Ollama)
- **Model**: LLaMA 3.2:1b
- **API**: Ollama REST API (`/api/generate`)
- **Purpose**: Natural language to SQL translation
- **Prompt Engineering**: Uses structured prompt template with database schema

### 3. **Database Layer** (MySQL)
- **Engine**: MySQL 8.0
- **Schema**: Sales order management
  - `users` table (id, name, email)
  - `orders` table (id, user_id, product, amount, order_date)
- **Sample Data**: Pre-populated with test users and orders

## Core Functions

### `ask_llama(question)`
**Purpose**: Interface with LLaMA model for SQL generation
- Formats user question with prompt template
- Sends HTTP POST request to Ollama API
- Returns generated SQL query as string

### `run_query(sql)`
**Purpose**: Execute SQL against MySQL database
- Establishes database connection
- Executes SQL query safely
- Returns columns and rows for SELECT queries
- Handles errors gracefully
- Manages connection cleanup

### `extract_sql(text)`
**Purpose**: Parse and clean SQL from LLM response
- Identifies SQL statements from mixed text
- Extracts valid SQL starting from SQL keywords
- Removes extraneous text/explanations

## Key Features

### 1. **Natural Language Interface**
- Users can ask questions in plain English
- Examples: "Show all orders", "What is the total sales amount?"

### 2. **Intelligent SQL Generation**
- Context-aware prompt includes database schema
- Generates syntactically correct MySQL queries
- Handles various query types (SELECT, aggregations, JOINs)

### 3. **Safety & Error Handling**
- Database connection error handling
- SQL execution error capture
- Graceful fallback for malformed queries

### 4. **User Experience**
- Real-time query execution with loading indicators
- Conversation history with query/result pairs
- Pre-defined sample questions for guidance
- Formatted SQL display with syntax highlighting

### 5. **Containerized Deployment**
- Docker Compose orchestration
- Service isolation (Streamlit, Ollama, MySQL)
- Environment-based configuration

## Environment Configuration

```bash
# LLM Service
LLAMA_API_URL=http://localhost:8000

# Database Connection
MYSQL_HOST=localhost
MYSQL_USER=salesuser
MYSQL_PASSWORD=salespass
MYSQL_DB=salesdb
```

## Use Cases

1. **Business Analytics**: Query sales data without SQL knowledge
2. **Data Exploration**: Interactive database exploration
3. **Training/Education**: Learn SQL through natural language examples
4. **Rapid Prototyping**: Quick database insights for decision making

## Technical Stack

- **Frontend**: Streamlit (Python web framework)
- **AI/ML**: LLaMA 3.2:1b via Ollama
- **Database**: MySQL 8.0
- **Containerization**: Docker & Docker Compose
- **Language**: Python 3.x

## Security Considerations

- Database credentials managed via environment variables
- SQL injection protection through parameterized queries
- Local LLM deployment (no external API calls)
- Network isolation via Docker containers

## Limitations

1. **Database Scope**: Limited to predefined schema (users/orders)
2. **Query Complexity**: May struggle with very complex SQL operations
3. **Model Size**: Uses lightweight LLaMA model (may affect accuracy)
4. **No Authentication**: No user access controls implemented

## Agent vs API Classification

**This is an AI Agent because it**:
- ✅ Has a specific domain (sales data querying)
- ✅ Performs autonomous actions (SQL generation & execution)
- ✅ Maintains state (conversation history)
- ✅ Has error handling and recovery mechanisms
- ✅ Provides intelligent responses based on context
- ✅ Integrates multiple systems (LLM + Database)

**It's NOT just an LLM API because**:
- ❌ It doesn't simply forward requests to an LLM
- ❌ It adds significant business logic
- ❌ It performs actions beyond text generation
- ❌ It has domain-specific knowledge and constraints

## Conclusion

This application represents a sophisticated **Text-to-SQL AI Agent** that demonstrates practical AI implementation for business use cases. It showcases how to combine modern LLMs with traditional databases to create intuitive, natural language interfaces for data querying.
