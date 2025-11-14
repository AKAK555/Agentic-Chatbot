from src.langgraphagenticai.state.state import State


class ChatbotWithToolNode:
    def __init__(self, model):
        self.llm = model
        
    def process(self, state: State) -> dict:
        user_input = state.get["messages"][-1] if state["messages"] else "" # Get the latest user message

        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])
        
        tools_response = f"Tool integration for: {user_input}"  # Placeholder for tool integration logic

        return {"messages": [llm_response, tools_response]}
    
    
    def create_chatbot(self, tools):
        """
        Returns a chatbot instance integrated with specified tools.
        
        """
        llm_with_tools = self.llm.bind_tools(tools)
        
        def chatbot_node(state: State):
            """Chatbot logic for processing input state and returning a response"""
            
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        
        return chatbot_node