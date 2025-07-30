import os
from autogen import ConversableAgent


api_base = "http://host.docker.internal:1234/v1"
config_list = [
    {
        "model": "google/gemma-3-4b",
        "base_url": api_base,
        'api_key': 'NULL',
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 1,
    "max_tokens": 1000,
    "parallel_tool_calls": False,
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