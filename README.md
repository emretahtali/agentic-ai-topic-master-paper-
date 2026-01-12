# agentic-ai-topic-master-paper
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
