import os
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent
from typing import Annotated

from dotenv import load_dotenv

load_dotenv()

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

traveler_agent = ConversableAgent(
    name="Traveler_Agent",
    system_message="You are a traveler planning a vacation.",
    llm_config=llm_config,
)

guide_agent = ConversableAgent(
    name="Guide_Agent",
    system_message="You are a travel guide with extensive knowledge about popular destinations. Give very short response with bullet points",
    llm_config=llm_config,
)

chat_result = traveler_agent.initiate_chat(
    guide_agent,
    message="What are the must-see attractions in Tokyo?",
    summary_method="reflection_with_llm",  # reflection_with_llm, reflection, llm -- see above explanations
    max_turns=2,
)

# print(chat_result)

# print(" \n ***Chat Summary***: \n")
# # summary is a property of the chat result
# print(chat_result.summary)

# print(" \nDefault Input Prompt: \n")
# # The input prompt for the LLM is the following default prompt:
# print(ConversableAgent.DEFAULT_SUMMARY_PROMPT)

# # Get the chat history.
# import pprint

# print(" \nChat history: \n")
# pprint.pprint(chat_result.chat_history)

# print(" \n**Chat Cost**: \n")
# # Get the cost of the chat.
# pprint.pprint(chat_result.cost)
