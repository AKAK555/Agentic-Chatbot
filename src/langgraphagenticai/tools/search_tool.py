from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Returns a list of tool nodes for the graph.
    Currently includes the Tavily Search tool.
    """
    tavily_search_tool = ToolNode(
        tools=TavilySearchResults(
            api_key="",  # API key to be set at runtime
            max_results=3,
            search_engine="google",
        ),
        name="Tavily Search Tool",
        description="A tool that uses Tavily Search to answer questions about current events and recent information.",
    )

    return [tavily_search_tool]

def create_tool_node(tools):
    """
    Creates a ToolNode that aggregates multiple tools.
    """
    def tool_process(state):
        
        tool_node = ToolNode(
            tool=tool_process,
            name="Aggregated Tool Node",
            description="A node that aggregates multiple tools for use in the graph.",
        )
        return tool_node