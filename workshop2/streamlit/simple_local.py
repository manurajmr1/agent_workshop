import autogen
from autogen import AssistantAgent, UserProxyAgent
import os
import openai

openai.api_base = "http://host.docker.internal:1234/v1"
# Define configuration using the OpenAI format expected by autogen
config_list = [
    {
        "model": "llama-3.2-3b-instruct",
        "base_url": openai.api_base,
        'api_key': 'NULL',
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 1,
    "parallel_tool_calls": False,
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
    human_input_mode="ALWAYS"
)

def run_agent():
    print("Autogen Local LM Studio Agent")
    print("Connected to: " + openai.api_base)
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
