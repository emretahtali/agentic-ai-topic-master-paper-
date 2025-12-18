import tiktoken
from langchain_core.messages import BaseMessage

ENC = tiktoken.get_encoding("o200k_base")


def _msg_text(m: BaseMessage) -> str:
    c = m.content
    if isinstance(c, list):
        parts = []
        for p in c:
            if isinstance(p, dict) and "text" in p:
                parts.append(p["text"])
            elif isinstance(p, str):
                parts.append(p)
            else:
                parts.append(str(p))
        return "\n".join(parts)
    return c or ""


def count_text(s: str) -> int:
    return len(ENC.encode(s or ""))


def count_messages(msgs: list[BaseMessage]) -> int:
    return sum(count_text(_msg_text(m)) for m in msgs)
