import os
from autogen import ConversableAgent
from typing import Annotated

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
# The Initial Agent always returns a given text.
initial_agent = ConversableAgent(
    name="Initial_Agent",
    system_message="You return me the text I give you.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Uppercase Agent converts the text to uppercase.
uppercase_agent = ConversableAgent(
    name="Uppercase_Agent",
    system_message="You convert the text I give you to uppercase.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Word Count Agent counts the number of words in the text.
word_count_agent = ConversableAgent(
    name="WordCount_Agent",
    system_message="You count the number of words in the text I give you.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)


# The Reverse Text Agent reverses the text.
reverse_text_agent = ConversableAgent(
    name="ReverseText_Agent",
    system_message="You reverse the text I give you.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Summarize Agent summarizes the text.
summarize_agent = ConversableAgent(
    name="Summarize_Agent",
    system_message="You summarize the text I give you.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# Start a sequence of two-agent chats.
# Each element in the list is a dictionary that specifies the arguments
# for the initiate_chat method.
chat_results = initial_agent.initiate_chats(
    [
        {
            "recipient": uppercase_agent,
            "message": "This is a sample text document.",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": word_count_agent,
            "message": "These are my numbers",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": reverse_text_agent,
            "message": "These are my numbers",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": summarize_agent,
            "message": "These are my numbers",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
    ]
)

print("First Chat Summary: ", chat_results[0].summary)
print("Second Chat Summary: ", chat_results[1].summary)
print("Third Chat Summary: ", chat_results[2].summary)
print("Fourth Chat Summary: ", chat_results[3].summary)