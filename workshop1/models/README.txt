# AI Sales Order Chatbot (Llama + MySQL + Streamlit)

## Overview
This project demonstrates an AI-powered chatbot that:
- Uses a local Llama 3.2:1b model (via Ollama) to generate SQL queries from natural language.
- Runs those queries against a MySQL sales order database.
- Provides a Streamlit web interface for chat, with a sidebar of sample questions.

## How it works
- The user asks a question in the chatbox (bottom of the page).
- The app sends a prompt to the Llama model via Ollama's API.
- The model returns only the SQL query (no explanation).
- The app runs the SQL on the MySQL database and displays the results in a table.
- All chat history is shown, with the most recent block at the top.
- The sidebar provides sample questions; clicking one fills the chatbox.

## How to run
1. **Download the Llama 3.2:1b model** using Ollama (the Docker Compose file will do this automatically).
2. **Start all services:**
   ```sh
   docker-compose up --build
   ```
3. **Open the app:**
   Go to [http://localhost:8501](http://localhost:8501) in your browser.

## MySQL Access
- Host: `localhost`
- Port: `3306`
- User: `salesuser`
- Password: `salespass`
- Database: `salesdb`

## Sample Questions
- Show all orders
- List users who bought a Laptop
- What is the total sales amount?
- Show all orders placed by Alice
- Get order amount for a specific product

## File Structure
- `docker-compose.yml` — Orchestrates MySQL, Ollama, and Streamlit services
- `mysql/init.sql` — Initializes the sales order schema and sample data
- `streamlit/app.py` — Streamlit chat UI and backend logic
- `streamlit/requirements.txt` — Python dependencies
- `models/` — (Optional) For custom model files if needed

## Notes
- The chat input is at the bottom, and the latest chat block appears at the top.
- The app is designed for demo/educational use and is not production-hardened.
