# GenAI Workshop 2: Building AI Agents with AutoGen

This workshop demonstrates how to build AI agents using AutoGen, a framework for building multi-agent systems with LLMs. The workshop includes examples of agents for travel planning, sequential text processing, and integration with external data sources like MySQL.

## Project Structure

```
workshop2/
├── docker-compose.yml        # Docker composition for MySQL and Streamlit services
├── mysql/
│   └── init.sql              # Initialization script for the travel database
└── streamlit/
    ├── app.py                # Main Streamlit application
    ├── Dockerfile            # Docker configuration for Streamlit
    ├── requirements.txt      # Python dependencies
    ├── seq_chat_agents.py    # Sequential chat agents example
    ├── simple_agent.py       # Basic agent implementation
    ├── simple_local.py       # Local model agent example
    ├── sum.py                # Simple sum calculation example
    ├── travel_planner_agents.py  # Travel planning agents
    ├── travel_tool.py        # Travel tools with mock data
    └── travel_tool_mysql.py  # Travel tools with MySQL integration
```

## Features

This workshop covers:

1. **Basic Agent Creation**: Learn how to create and configure basic AI agents
2. **Multi-Agent Systems**: Implement communication between multiple specialized agents
3. **Sequential Processing**: Build a chain of agents that process data sequentially
4. **External Tools Integration**: Connect agents to external data sources (MySQL)
5. **Local Model Integration**: Run agents with local LLM models

## Examples Included

### 1. Simple Agent

A basic example of creating an AutoGen agent and generating a response.

### 2. Travel Planner Agents

A traveler agent and a guide agent that interact to provide travel recommendations.

```python
# Example usage:
traveler_agent.initiate_chat(
    guide_agent,
    message="What are the must-see attractions in Tokyo?",
)
```

### 3. Sequential Chat Agents

A pipeline of 4 agents that process text sequentially:
- TextSanitizer (removes special characters and numbers)
- TextUppercaser (converts text to uppercase)
- TextCleanser (removes extra spaces)
- SpaceRemover (removes all spaces)

### 4. Travel Tools with MySQL Integration

Travel-related tools that fetch real data from a MySQL database:
- Flight status lookup
- Hotel information retrieval
- Travel advice for destinations

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- OpenAI API key (for some examples)

### Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd workshop2
   ```

2. Set up environment variables (create a `.env` file in the streamlit directory):
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Start the services with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the Streamlit application:
   Open your browser and navigate to http://localhost:8501

### Running Examples Individually

You can run individual agent examples directly:

```bash
cd streamlit
python travel_planner_agents.py
python seq_chat_agents.py
```

## Database Structure

The MySQL database includes tables for:
- `flight_status`: Information about flight numbers and their status
- `hotels`: Details about hotels in various locations
- `travel_advice`: Travel recommendations for different destinations

## Technologies Used

- **AutoGen**: Framework for building multi-agent systems
- **Streamlit**: Web application framework for the user interface
- **MySQL**: Database for storing travel-related information
- **Docker**: Containerization for easy deployment
- **Python**: Programming language for all examples

## Advanced Usage

### Connecting to Local LLM Models

Some examples show how to connect to local LLM models using an API endpoint:

```python
api_base = "http://host.docker.internal:1234/v1"
config_list = [
    {
        "model": "google/gemma-3-4b",
        "base_url": api_base,
        'api_key': 'NULL',
    }
]
```

### Setting Up LM Studio for Local Model Inference

This workshop uses LM Studio to run local models, which provides an OpenAI-compatible API endpoint for AutoGen to connect to.

1. **Install LM Studio**:
   - Download from [https://lmstudio.ai/](https://lmstudio.ai/)
   - Install and launch the application

2. **Download the Gemma-3-4b Model**:
   - In LM Studio, go to the "Models" tab
   - Search for "google/gemma-3-4b"
   - Download the model

3. **Configure the Model with Custom Prompt Template**:
   - Select the downloaded Gemma-3-4b model
   - Go to "Local Inference Server" settings
   - Set the server port to 1234 (matching our code configuration)
   - In the "Advanced" section, find "Custom Chat Template" and paste the following template:

```
{{ bos_token }} {%- if messages[0]['role'] == 'system' -%} {%- if messages[0]['content'] is string -%} {%- set first_user_prefix = messages[0]['content'] + '\n' -%} {%- else -%} {%- set first_user_prefix = messages[0]['content'][0]['text'] + '\n' -%} {%- endif -%} {%- set loop_messages = messages[1:] -%} {%- else -%} {%- set first_user_prefix = "" -%} {%- set loop_messages = messages -%} {%- endif -%} {%- for message in loop_messages -%} {%- if (message['role'] == 'assistant') -%} {%- set role = "model" -%} {%- else -%} {%- set role = message['role'] -%} {%- endif -%} {{ '<start_of_turn>' + role + '\n' + (first_user_prefix if loop.first else "") }} {%- if message['content'] is string -%} {{ message['content'] | trim }} {%- elif message['content'] is iterable -%} {%- for item in message['content'] -%} {%- if item['type'] == 'image' -%} {{ '<start_of_image>' }} {%- elif item['type'] == 'text' -%} {{ item['text'] | trim }} {%- endif -%} {%- endfor -%} {%- else -%} {{ raise_exception("Invalid content type") }} {%- endif -%} {{ '<end_of_turn>\n' }} {%- endfor -%} {%- if add_generation_prompt -%} {{'<start_of_turn>model\n'}} {%- endif -%}
```

4. **Start the Local Server**:
   - Click "Start Server" in LM Studio
   - The server will be accessible at http://localhost:1234/v1
   - AutoGen code can now connect to this endpoint

5. **Verify Connection**:
   - Run a simple test from the workshop examples:
   ```bash
   cd streamlit
   python simple_agent.py
   ```
   - You should see a response generated by your local Gemma-3-4b model

> **Note**: Using a local model with LM Studio provides privacy benefits and eliminates the need for API keys, but requires more computational resources.

### Custom Tool Creation

The workshop demonstrates how to create custom tools for agents:

```python
def get_flight_status(flight_number: Annotated[str, "Flight number"]) -> str:
    # Implementation for retrieving flight status
```

## Resources

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
