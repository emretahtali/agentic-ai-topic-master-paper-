from mcp_client.util import mcp_client
from langchain_core.tools.base import ToolException
from pydantic import ValidationError
import json

from agentic_network.agents import Agent
from agentic_network.core import AgentState


class ToolsAgent(Agent):
    def __init__(self):
        tools = mcp_client.get_tools()
        self.tools_by_name = {t.name: t for t in tools}

        for t in tools:
            if not hasattr(t, "handle_tool_error"): continue
            t.handle_tool_error = lambda e: f"TOOL_ERROR: {e}"

    async def _get_node(self, agent_state: AgentState) -> dict:
        print("\n---TOOLS AGENT---")

        agent_action = agent_state["agent_outcome"]
        tool_name = getattr(agent_action, "tool", None) or agent_action.get("tool")
        raw_input = getattr(agent_action, "tool_input", None) or agent_action.get("tool_input")

        output = ""
        tool_to_call = self.tools_by_name.get(agent_action.tool)

        if tool_to_call is None:
            observation = self._format_tool_error(
                tool_name or "(missing)",
                "Tool not found.",
                raw_input,
            )
            print("Tool output:", observation)
            return {"intermediate_steps": [(agent_action, observation)]}

        # Normalize inputs first (turn malformed inputs into observation, not exceptions)
        args, parse_err = ToolsAgent._normalize_args(raw_input)
        if parse_err:
            observation = self._format_tool_error(tool_name, parse_err, raw_input)
            print("Tool output:", observation)
            return {"intermediate_steps": [(agent_action, observation)]}

        # Call the tool safely; convert *any* exception into an observation
        try:
            result = await tool_to_call.ainvoke(args)
            observation = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)

        except ToolException as e:
            observation = self._format_tool_error(tool_name, str(e), args)

        except ValidationError as e:
            # Common case: missing or wrong-typed args
            observation = self._format_tool_error(tool_name, f"ValidationError: {e}", args)

        except Exception as e:
            observation = self._format_tool_error(tool_name, f"{type(e).__name__}: {e}", args)

        print("Tool output:", observation)
        return {"intermediate_steps": [(agent_action, observation)]}

    def _format_tool_error(self, tool_name: str, msg: str, args) -> str:
        """Uniform observation text the LLM can act on immediately."""
        hint = (
            "Lütfen aynı aracı sadece geçerli argümanlar kullanarak yeniden çağır. "
            "Tanımlanmamış key'ler kullanma. Tam ve kesin key adlarını kullan. "
            "Customer no için her zaman 17976826 kullan. "
            "Action Input yalnızca tek bir JSON nesnesi olmalı; kod blokları (```), yorum, trailing virgül YOK. "
            "Action Input yalnızca tek bir JSON nesnesi olmalı; kod blokları (```), yorum, trailing virgül KULLANMA. "
            "Action Input yalnızca tek bir JSON nesnesi olmalı; kod blokları (```), yorum, trailing virgül YOK. "
        )
        args_str = json.dumps(args, ensure_ascii=False) if isinstance(args, (dict, list)) else str(
            args)

        return (
            f"TOOL_ERROR\n"
            f"tool: {tool_name}\n"
            f"message: {msg}\n"
            f"expected_args:\n{ToolsAgent._format_schema(self.tools_by_name.get(tool_name) or None)}\n"
            f"your_args: {args_str}\n"
            f"hint: {hint}"
        )

    @staticmethod
    def _format_schema(tool) -> str:
        """Best-effort summary of expected args for the agent."""

        if tool is None:
            return "No schema available."

        schema_lines = []
        schema = None

        # LangChain BaseTool usually exposes args_schema (Pydantic model) or input_schema
        args_schema = getattr(tool, "args_schema", None)
        input_schema = getattr(tool, "input_schema", None)

        if args_schema is not None:
            # Pydantic v2: model_fields; v1: __fields__
            fields = getattr(args_schema, "model_fields", None) or getattr(args_schema, "__fields__", {})
            for name, field in (fields.items() if isinstance(fields, dict) else []):
                # v2 style
                required = getattr(field, "is_required", lambda: getattr(field, "required", False))()
                typ = getattr(field, "annotation", None) or getattr(field, "outer_type_", None)
                schema_lines.append(
                    f"- {name} ({getattr(typ, '__name__', str(typ))}){' [required]' if required else ''}")

        elif input_schema is not None:
            # JSON schema-like structure
            req = set(input_schema.get("required", []))
            props = input_schema.get("properties", {})
            for name, meta in props.items():
                typ = meta.get("type", "any")
                schema_lines.append(f"- {name} ({typ}){' [required]' if name in req else ''}")

        if schema_lines: schema = "\n".join(schema_lines)
        return schema or "(no argument schema available)"

    @staticmethod
    def _normalize_args(raw):
        """
        Accept dict, JSON string, or empty/None.
        Returns (args_dict, error_str_or_None)
        """
        if raw is None:
            return {}, None

        if isinstance(raw, dict):
            return raw, None

        if isinstance(raw, str):
            s = raw.strip()
            if s.lower() in ("", "none", "null"):
                return {}, None

            # Try JSON
            try:
                val = json.loads(s)

                if isinstance(val, dict):
                    return val, None

                # If it's JSON but not an object, treat as error so the LLM fixes it.
                return None, f"Tool input must be a JSON object (key/value), got {type(val).__name__}"

            except json.JSONDecodeError as e:
                return None, f"Tool input is a malformed JSON string: {e}"

        # Unexpected type
        return None, f"Tool input must be a dict or JSON object string, got {type(raw).__name__}"
