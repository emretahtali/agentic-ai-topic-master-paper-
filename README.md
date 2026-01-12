# agentic-ai-topic-master-paper
A multi-agent orchestration system built with **Python**, **LangGraph**, **LangChain**, and **FastAPI**. This project implements a **Topic Master Architecture**, a nested graph topology that dynamically routes user intent to specialized expert agents (such as Diagnosis and Appointment) while maintaining complex conversational state.

## Repository Structure
```
Repository Structure (src):
├── __init__.py
├── agentic_network
│   ├── __init__.py
│   ├── agent_graph.py
│   ├── agents
│   │   ├── __init__.py
│   │   ├── agent_data.py
│   │   ├── appointment
│   │   │   ├── __init__.py
│   │   │   ├── appointment_agent.py
│   │   │   └── system_prompt.py
│   │   ├── diagnosis
│   │   │   ├── __init__.py
│   │   │   ├── diagnosis_agent.py
│   │   │   └── system_prompt.py
│   │   ├── post_processing_agent.py
│   │   ├── pre_processing_agent.py
│   │   ├── tools_agent.py
│   │   └── topic_manager_cluster
│   │       ├── __init__.py
│   │       ├── agents
│   │       │   ├── __init__.py
│   │       │   ├── new_topic_agent.py
│   │       │   ├── post_processing_agent.py
│   │       │   ├── pre_processing_agent.py
│   │       │   ├── previous_topics_checker_agent.py
│   │       │   ├── router_agent.py
│   │       │   └── topic_change_checker_agent.py
│   │       ├── core
│   │       │   ├── __init__.py
│   │       │   ├── topic_manager_routes.py
│   │       │   └── topic_manager_state.py
│   │       ├── routing
│   │       │   ├── __init__.py
│   │       │   └── decide_topic_selected.py
│   │       ├── topic_manager_cluster.py
│   │       └── utils
│   │           ├── __init__.py
│   │           └── topic_manager_util.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── agent_state.py
│   │   └── routes.py
│   ├── routing
│   │   ├── __init__.py
│   │   └── tools_condition.py
│   └── utils
│       ├── __init__.py
│       ├── base_agent.py
│       ├── base_utils.py
│       ├── custom_react_agent.py
│       ├── custom_react_parser.py
│       └── tokenizer.py
├── fastapi_server
│   ├── __init__.py
│   ├── assistant_service.py
│   ├── invoke_body.py
│   ├── server_controller.py
│   └── server_main.py
├── llm
│   ├── __init__.py
│   ├── client_types
│   │   ├── __init__.py
│   │   ├── llm_client_appointment.py
│   │   ├── llm_client_diagnosis.py
│   │   ├── llm_client_gemini.py
│   │   ├── llm_client_openai.py
│   │   └── llm_client_topic_master.py
│   ├── devices.py
│   ├── llm_client.py
│   └── models.py
├── main.py
└── mcp_client
    ├── __init__.py
    ├── appointment_mcp.py
    ├── diagnosis_mcp.py
    └── util
        ├── __init__.py
        └── mcp_client.py
```

## Key Features

* **Topic Master Architecture:** A nested graph orchestrator that manages conversation state using a "Topic Stack," ensuring context retention across multi-turn dialogues.
* **Model Context Protocol (MCP):** Connects agents to external tools (Diagnosis and Appointment servers) dynamically.
* **FastAPI Streaming Server:** Supports both synchronous (`/invoke`) and WebSocket streaming (`/stream`) endpoints.
* **Model Agnostic:** Configurable to run with Google Gemini, OpenAI, or DeepInfra.

## 🛠️ Prerequisites

* Python 3.10+
* [uv](https://docs.astral.sh/uv/) (Recommended for dependency management)

## ⚙️ Configuration

Create a `.env` file in the root directory. Configure the following variables based on your LLM provider and server needs:

```env
# Server Configuration
AGENTIC_SERVER_HOST=0.0.0.0
AGENTIC_SERVER_PORT=8082
AGENTIC_SERVER_API_KEY=your-secure-server-key

# Model Context Protocol (MCP) Ports
APPOINTMENT_SERVER_PORT=8081
DIAGNOSIS_SERVER_PORT=8080

# --- LLM Configurations (Example for Gemini) ---
GEMINI_API_KEY=your_google_api_key
GEMINI_API_MODEL=gemini-2.5-flash
GEMINI_API_ENDPOINT=[https://generativelanguage.googleapis.com](https://generativelanguage.googleapis.com)

# Topic Master Specific LLM (Routing Logic)
TOPIC_MASTER_LLM_TYPE=GEMINI
TOPIC_MASTER_LLM_API_KEY=your_google_api_key
TOPIC_MASTER_LLM_MODEL_NAME=gemini-2.5-flash

# Diagnosis Agent LLM
DIAGNOSIS_LLM_TYPE=GEMINI
DIAGNOSIS_LLM_API_KEY=your_google_api_key
DIAGNOSIS_LLM_MODEL_NAME=medgemma-27b # or relevant model

# Appointment Agent LLM
APPOINTMENT_LLM_TYPE=GEMINI
APPOINTMENT_LLM_API_KEY=your_google_api_key
```

## 🚀 Usage

### 1. Install Dependencies
```bash
uv sync
```

### 2. Run the Server
You can start the FastAPI server using the provided entry point:

```bash
uv run python -m fastapi_server.server_main
```

The server will start on `0.0.0.0:8082` (or your configured port).

### 3. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/healthz` | Health check. |
| `POST` | `/invoke` | Single-turn invocation. Requires `thread_id` and `input` payload. |

**Example Payload (`/invoke`):**
```json
{
  "thread_id": UUID,
  "client_turn_id": UUID,
  "input": {
    "message": "I have a severe headache and need to see a doctor."
  }
}
```

