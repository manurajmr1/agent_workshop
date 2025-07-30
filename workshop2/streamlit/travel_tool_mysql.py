import os
import logging
import mysql.connector
from autogen import ConversableAgent
from typing import Annotated
from dotenv import load_dotenv

# Suppress autogen warnings
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

load_dotenv()

# MySQL configuration
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "salesuser")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "salespass")
MYSQL_DB = os.environ.get("MYSQL_DB", "salesdb")

def query_execute(table: str, column: str, value: str, result_column: str = None):
    """
    Common MySQL query function to fetch data from travel tables
    
    Args:
        table: The table name to query
        column: The column to search in
        value: The value to search for
        result_column: The column to return (if None, returns all columns)
    
    Returns:
        Query result or None if not found
    """
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        cursor = connection.cursor(dictionary=True)
        
        if result_column:
            query = f"SELECT {result_column} FROM {table} WHERE {column} = %s"
        else:
            query = f"SELECT * FROM {table} WHERE {column} = %s"
        
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return result
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
api_base = "http://host.docker.internal:1234/v1"
config_list = [
    {
        "model": "google/gemma-3-4b",
        "base_url": api_base,
        'api_key': 'NULL',
        "price": [0, 0],  # [prompt_price_per_1k, completion_token_price_per_1k]
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 1,
    "max_tokens": 1000,
    "parallel_tool_calls": False,
}


def get_flight_status(flight_number: Annotated[str, "Flight number"]) -> str:
    result = query_execute("flight_status", "flight_number", flight_number, "status")
    if result:
        return f"The current status of flight {flight_number} is {result['status']}."
    else:
        return f"The current status of flight {flight_number} is unknown."


def get_hotel_info(location: Annotated[str, "Location"]) -> str:
    result = query_execute("hotels", "location", location)
    if result:
        return f"Top hotel in {location}: {result['hotel_name']} - {result['stars']} stars"
    else:
        return f"No hotels found in {location}."


def get_travel_advice(location: Annotated[str, "Location"]) -> str:
    result = query_execute("travel_advice", "location", location, "advice")
    if result:
        return result['advice']
    else:
        return f"No travel advice available for {location}."


# Define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="TravelAssistant",
    system_message="You are a helpful AI travel assistant. Return 'TERMINATE' when the task is done.",
    llm_config=llm_config,
)



# The user proxy agent is used for interacting with the assistant agent and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    is_termination_msg=lambda msg: msg.get("content") is not None
    and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register the tool signatures with the assistant agent.
assistant.register_for_llm(
    name="get_flight_status",
    description="Get the current status of a flight based on the flight number",
)(get_flight_status)
assistant.register_for_llm(
    name="get_hotel_info",
    description="Get information about hotels in a specific location",
)(get_hotel_info)
assistant.register_for_llm(
    name="get_travel_advice", description="Get travel advice for a specific location"
)(get_travel_advice)

# Register the tool functions with the user proxy agent.
user_proxy.register_for_execution(name="get_flight_status")(get_flight_status)
user_proxy.register_for_execution(name="get_hotel_info")(get_hotel_info)
user_proxy.register_for_execution(name="get_travel_advice")(get_travel_advice)

user_proxy.initiate_chat(
    assistant,
    message="I need help with my travel plans. Can you help me? I am traveling to New York. I need hotel information. Also give me the status of my flight AA123. Also give me some travel advice for new York.",
)