import autogen
from autogen import AssistantAgent, UserProxyAgent
import os
import openai

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

# Create the assistant agent (LLM)
assistant = AssistantAgent(
    name="LocalModelAssistant",
    llm_config=llm_config,
    system_message="You are a helpful assistant. Use your knowledge and tools to answer user questions."
)

# Create the user proxy agent
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    code_execution_config=False,
)

def run_agent():
    print("Autogen Local LM Studio Agent")
    print("Connected to GEMINI" )
    print("Type 'exit' to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        # Start the conversation
        user_proxy.initiate_chat(
            assistant,
            message=user_input,
            max_turns=2
        )

if __name__ == "__main__":
    run_agent()
