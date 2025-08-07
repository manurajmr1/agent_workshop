import os
from autogen import ConversableAgent
from typing import Annotated
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

# Old configuration - commented out
# api_base = "http://host.docker.internal:1234/v1"
# config_list = [
#     {
#         "model": "qwen/qwen3-4b",
#         "base_url": api_base,
#         'api_key': 'NULL'
#     }
# ]
# 
# llm_config = {
#     "config_list": config_list
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



# The Initial Agent always returns a given text.
initial_agent = ConversableAgent(
    name="Initial_Agent",
    system_message="You return me the text I give you enable_thinking=False",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Uppercase Agent converts the text to uppercase.
uppercase_agent = ConversableAgent(
    name="Uppercase_Agent",
    system_message="You convert the text I give you to uppercase. And return converted text in quotes",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Word Count Agent counts the number of words in the text.
word_count_agent = ConversableAgent(
    name="WordCount_Agent",
    system_message="You count the number of words in the original text I give you not reversed text. For the sentence in quotes.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)


# The Reverse Text Agent reverses the text.
reverse_text_agent = ConversableAgent(
    name="ReverseText_Agent",
    system_message="You take the words in and write them reverse order. For the sentence in quotes.",
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
            "max_turns": 1,
            "summary_method": "last_msg",
        },
        {
            "recipient": reverse_text_agent,
            "message": "Take the words in and write them reverse order in the text below in quotes.",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
        {
            "recipient": word_count_agent,
            "message": "Find the count of words in the original text below in quotes.",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
    ]
)

print("First Chat Summary: ", chat_results[0].summary)
print("Second Chat Summary: ", chat_results[1].summary)
print("Third Chat Summary: ", chat_results[2].summary)
