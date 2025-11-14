import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


import streamlit as st
import re
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class DisplayResultStreamlit:
    def __init__(self, usecase, graph):
        self.usecase = usecase
        self.graph = graph

    def _extract_content_from_str(self, msg_str):
        # Extract content='...' from the string representation of message
        match = re.search(r"content='(.*?)(?<!\\)'", msg_str)
        if match:
            # Unescape any escaped single quotes
            content = match.group(1).replace("\\'", "'")
            return content
        return msg_str  # fallback to raw string if pattern not matched

    def display_result_on_ui(self, user_message):
        user_message = user_message.strip()
        if not user_message:
            st.warning("Please enter a message before running the chatbot.")
            return

        # Display user message once
        with st.chat_message("user"):
            st.write(user_message)

        # try:
        #     events = self.graph.stream({'messages': [{"role": "user", "content": user_message}]})
        #     st.write("DEBUG: Raw events from graph.stream()")
        #     for event in events:
        #         st.write(event)  # Show raw data for debugging
        #         for value in event.values():
        #             messages = value.get('messages', [])
        #             if not isinstance(messages, list):
        #                 messages = [messages]

        #             for msg in messages:
        #                 content = None
        #                 if isinstance(msg, str):
        #                     # Parse string representations of message objects
        #                     content = self._extract_content_from_str(msg)
        #                 else:
        #                     if hasattr(msg, "content"):
        #                         content = msg.content
        #                     elif isinstance(msg, dict):
        #                         content = msg.get("content")
        #                     else:
        #                         content = str(msg)

        #                 if content:
        #                     with st.chat_message("assistant"):
        #                         st.write(content)

        # except Exception as e:
        #     st.error(f"Error during streaming: {e}")

        if self.usecase == "Basic Chatbot":
            try:
                for event in self.graph.stream({'messages': [{"role": "user", "content": user_message}]}):
                    st.write("DEBUG event:", event)
                    for value in event.values():
                        messages = value.get('messages', [])
                        if not isinstance(messages, list):
                            messages = [messages]

                        for msg in messages:
                            content = None
                            if hasattr(msg, "content"):
                                content = msg.content
                            elif isinstance(msg, dict):
                                content = msg.get("content")
                            else:
                                content = str(msg)

                            if content:
                                with st.chat_message("assistant"):
                                    st.write(content)
            except Exception as e:
                st.error(f"Error during streaming: {e}")

        elif self.usecase == "Chatbot With Tool":
            try:
                initial_state = {"messages": [user_message]}
                res = self.graph.invoke(initial_state)
                for message in res.get('messages', []):
                    if isinstance(message, HumanMessage):
                        with st.chat_message("user"):
                            st.write(message.content)
                    elif isinstance(message, ToolMessage):
                        with st.chat_message("ai"):
                            st.write("Tool Call Start")
                            st.write(message.content)
                            st.write("Tool Call End")
                    elif isinstance(message, AIMessage) and message.content:
                        with st.chat_message("assistant"):
                            st.write(message.content)
            except Exception as e:
                st.error(f"Error during Chatbot With Tool invocation: {e}")

        elif self.usecase == "AI News":
            try:
                frequency = user_message.lower()
                with st.spinner("Fetching and summarizing news... ⏳"):
                    result = self.graph.invoke({"messages": frequency})
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()
                    st.markdown(markdown_content, unsafe_allow_html=True)
            except FileNotFoundError:
                st.error(f"News file not found for query '{frequency}': {AI_NEWS_PATH}")
            except Exception as e:
                st.error(f"Error fetching AI news: {e}")


# Streamlit app entry point
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.LLMS.groqllm import GroqLLM  # Import your GroqLLM class


def main():
    st.title("🤖 Chatbot")

    # Sidebar controls for API key and model selection
    groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    selected_groq_model = st.sidebar.selectbox(
        "Select Groq Model",
        options=["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "openai/gpt-oss-20b"]  
    )

    user_controls_input = {
        "GROQ_API_KEY": groq_api_key,
        "selected_groq_model": selected_groq_model,
    }

    # Use case selector in sidebar
    usecase = st.sidebar.selectbox("Select use case:", ["Basic Chatbot", "Chatbot with Tool", "AI News"])

    if not groq_api_key:
        st.warning("Please enter your Groq API key in the sidebar.")
        return

    # Initialize GroqLLM with user controls
    groq_llm_wrapper = GroqLLM(user_controls_input)
    try:
        llm = groq_llm_wrapper.get_llm_models()
    except Exception as e:
        st.error(f"Failed to initialize GroqLLM: {e}")
        return

    # Build graph with the initialized llm
    graph_builder = GraphBuilder(llm)
    try:
        compiled_graph = graph_builder.setup_graph(usecase)
    except Exception as e:
        st.error(f"Error building computation graph: {e}")
        return

    # Initialize display handler
    display_result = DisplayResultStreamlit(usecase, compiled_graph)

    # User input and send button
    user_input = st.text_input("Enter your message:", key="user_input")

    if st.button("Send"):
        if user_input and user_input.strip():
            display_result.display_result_on_ui(user_input.strip())
        else:
            st.warning("Please enter a message before sending.")


if __name__ == "__main__":
    main()
