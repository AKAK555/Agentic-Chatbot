# basic_chatbot_node.py
from typing import Any, List, Dict, Union
from src.langgraphagenticai.state.state import State
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class BasicChatbotNode:
    """
    Basic Chatbot node:
    - expects a State with a 'messages' list (or fallback keys 'user_input'/'text')
    - normalizes inputs to langchain message objects
    - invokes the provided LLM via self.llm.invoke()
    - returns {"messages": [ ...existing..., assistant_reply ]}
    """

    def __init__(self, model: Any):
        self.llm = model

    def _normalize_input(self, raw: Union[List, str, None]) -> List:
        """Normalize raw input into a list of Message objects."""
        normalized: List = []

        # single string -> user message
        if isinstance(raw, str):
            if raw.strip():
                return [HumanMessage(content=raw.strip())]
            return []

        # if not list-like, return empty
        if not isinstance(raw, (list, tuple)):
            return []

        for item in raw:
            # flatten nested lists/tuples one level
            if isinstance(item, (list, tuple)):
                for sub in item:
                    normalized.extend(self._normalize_input(sub))
                continue

            if isinstance(item, (HumanMessage, AIMessage, ToolMessage)):
                normalized.append(item)
                continue

            if isinstance(item, dict):
                role = item.get("role", "user")
                content = item.get("content") or item.get("text") or ""
                if role == "user":
                    normalized.append(HumanMessage(content=str(content)))
                elif role == "assistant":
                    normalized.append(AIMessage(content=str(content)))
                else:
                    # fallback to HumanMessage but include role marker
                    normalized.append(HumanMessage(content=f"[{role}] {content}"))
                continue

            if isinstance(item, str):
                normalized.append(HumanMessage(content=item))
                continue

            # fallback: stringify
            normalized.append(HumanMessage(content=str(item)))

        return normalized

    def _normalize_response(self, resp: Any) -> AIMessage:
        """Ensure the LLM response is an AIMessage."""
        if isinstance(resp, AIMessage):
            return resp
        if isinstance(resp, HumanMessage) or isinstance(resp, ToolMessage):
            return AIMessage(content=getattr(resp, "content", str(resp)))
        if isinstance(resp, str):
            return AIMessage(content=resp)
        # fallback
        return AIMessage(content=str(resp))

    def process(self, state: State) -> Dict:
        """
        Process the input state and generate a chatbot response.
        Returns a dict with key 'messages' that is a non-empty list of message objects.
        """

        # Accept dict-like State or object with attributes
        raw_messages = None
        if hasattr(state, "get"):
            raw_messages = state.get("messages", None)
        else:
            # support attribute-style State if used elsewhere
            raw_messages = getattr(state, "messages", None)

        # fallback: try user_input or text
        if not raw_messages:
            if hasattr(state, "get"):
                fallback = state.get("user_input") or state.get("text")
            else:
                fallback = getattr(state, "user_input", None) or getattr(state, "text", None)
            if fallback:
                raw_messages = [fallback]

        # Normalize input messages
        normalized_in = self._normalize_input(raw_messages)

        if not normalized_in:
            # If still empty, raise a clear error for the caller (UI should prevent this)
            raise ValueError("State must include a non-empty 'messages' list or provide 'user_input'/'text'.")

        # Invoke LLM - pass normalized message objects (adapter should accept these)
        try:
            response = self.llm.invoke(normalized_in)
        except Exception as exc:
            # re-raise with context
            raise RuntimeError(f"LLM invocation failed: {exc}") from exc

        # Normalize LLM response to AIMessage
        ai_msg = self._normalize_response(response)

        # Append assistant message to conversation
        final_messages = list(normalized_in) + [ai_msg]

        return {"messages": final_messages}
