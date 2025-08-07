import os
from autogen import ConversableAgent

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


agent = ConversableAgent(
    name="chatbot",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)

response = agent.generate_reply(
    messages=[{"role": "user", "content": "Tell me a funny joke."}]
)
print(response)