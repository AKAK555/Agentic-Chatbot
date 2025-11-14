# state.py
from typing import Any, List
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represent the structure of the state used in the graph.

    The 'messages' key is a list of items (message dicts / Message objects / strings).
    The add_messages annotation is preserved for any langgraph validators/hooks.
    """
    messages: Annotated[List[Any], add_messages]
