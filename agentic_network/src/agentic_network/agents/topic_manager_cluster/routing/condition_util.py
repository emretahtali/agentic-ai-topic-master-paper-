from agentic_network.core import AgentState


def strip_braces(s: str) -> str:
    s = s.strip()

    if s.startswith("{"):
        if s.endswith("}"): s =  s[1:-1].strip()
        else: s = s[1:].strip()
    elif s.endswith("}"): s = s[:-1].strip()

    if s.startswith("["):
        if s.endswith("]"): s =  s[1:-1].strip()
        else: s = s[1:].strip()
    elif s.endswith("]"): s = s[:-1].strip()

    return s


def clean_thoughts(agent_state: AgentState):
    agent_state["thoughts"].clear()