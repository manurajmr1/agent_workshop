import os
import logging
from autogen import ConversableAgent
from typing import Annotated
from dotenv import load_dotenv

# Suppress autogen warnings
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

load_dotenv()

# api_base = os.environ.get("LM_STUDIO_API_URL", "http://host.docker.internal:1234/v1")
# config_list = [
#     {
#         "model": "google/gemma-3-4b",
#         "base_url": api_base,
#         'api_key': 'NULL',
#     }
# ]

# llm_config = {
#     "config_list": config_list,
#     "temperature": 1,
#     "max_tokens": 1000,
#     "parallel_tool_calls": False,
# }

# New configuration using Gemini model
config_list = [
    {
        "model": "gemini-2.5-flash-lite",
        "api_type": "google",
        "api_key": os.getenv("GEMINI_API_KEY")
    }
]

llm_config = {
    "config_list": config_list
}


def get_flight_status(flight_number: Annotated[str, "Flight number"]) -> str:
    dummy_data = {"AA123": "On time", "DL456": "Delayed", "UA789": "Cancelled"}
    return f"The current status of flight {flight_number} is {dummy_data.get(flight_number, 'unknown')}."


def get_hotel_info(location: Annotated[str, "Location"]) -> str:
    dummy_data = {
        "New York": "Top hotel in New York: The Plaza - 5 stars",
        "Los Angeles": "Top hotel in Los Angeles: The Beverly Hills Hotel - 5 stars",
        "Chicago": "Top hotel in Chicago: The Langham - 5 stars",
    }
    return dummy_data.get(location, f"No hotels found in {location}.")


def get_travel_advice(location: Annotated[str, "Location"]) -> str:
    dummy_data = {
        "New York": "Travel advice for New York: Visit Central Park and Times Square.",
        "Los Angeles": "Travel advice for Los Angeles: Check out Hollywood and Santa Monica Pier.",
        "Chicago": "Travel advice for Chicago: Don't miss the Art Institute and Millennium Park.",
    }
    return dummy_data.get(location, f"No travel advice available for {location}.")


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