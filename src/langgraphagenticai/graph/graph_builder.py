# graph_builder.py
from langgraph.graph import StateGraph, START, END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition, ToolNode
from src.langgraphagenticai.nodes.chatbot_with_Tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    """
    Builds a graph for the selected use case.
    Only minimal fixes applied — no structural changes.
    """

    def __init__(self, model):
        self.llm = model
        # Initialize the graph builder using the State type
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class
        and integrates it into the graph. The chatbot node is set as both the
        entry and exit point of the graph.
        """
        try:
            chatbot_node = BasicChatbotNode(self.llm)

            # ✅ Defensive: wrap chatbot_node.process so it always returns {'messages': list}
            def safe_process(state):
                result = chatbot_node.process(state)
                # Normalize output to prevent empty or incorrect structures
                if not isinstance(result, dict):
                    result = {"messages": []}
                if "messages" not in result:
                    result["messages"] = []
                # Ensure messages list is not empty — prevents "'messages' minimum number of items is 1" error
                if not result["messages"]:
                    from langchain_core.messages import AIMessage
                    result["messages"] = [AIMessage(content="No response generated.")]
                return result

            self.graph_builder.add_node("chatbot", safe_process)
            self.graph_builder.add_edge(START, "chatbot")
            self.graph_builder.add_edge("chatbot", END)

        except Exception as e:
            raise RuntimeError(f"Error while building basic chatbot graph: {e}")

    def chatbot_with_tool_build_graph(self):
        """
        Builds a chatbot with tool graph using LangGraph.
        """
        tools = get_tools()
        tool_node = create_tool_node(tools)
        
        llm = self.llm
        
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)
        
        
        self.graph_builder.add_node("chatbot", "")
        self.graph_builder.add_node("tool_node", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_builder_graph(self):
        
        ai_news_node = AINewsNode(self.llm)
        
        # Builds an AI News Generator graph using LangGraph.
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)
        
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)

    def setup_graph(self, usecase: str):
        """
        Sets up and compiles the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot with Tool":
            self.basic_chatbot_build_graph()
        elif usecase == "AI News":
            self.ai_news_builder_graph()
        else:
            raise ValueError(f"Unsupported use case: {usecase}")

        # Compile and return the built graph
        try:
            compiled_graph = self.graph_builder.compile()
            return compiled_graph
        except Exception as e:
            raise RuntimeError(f"Failed to compile the graph: {e}")
