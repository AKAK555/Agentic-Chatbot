# main.py
import streamlit as st
import traceback

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit


def load_langgraph_agenticai_app():
    """Load and run the LangGraph Agentic AI Streamlit application."""
    st.set_page_config(layout="wide")
    ui = LoadStreamlitUI()
    user_controls = ui.load_streamlit_ui()

    if not user_controls:
        st.warning("Please make selections in the sidebar to proceed.")
        return {}

    usecase = user_controls.get("selected_usecase")
    if not usecase:
        st.warning("Please select a use case to proceed.")
        return {}

    # Prefer the persisted textarea input from the UI (if present)
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message:")

    if not user_message:
        # nothing to do
        return {}

    try:
        obj_llm_config = GroqLLM(user_controls_input=user_controls)
        model = obj_llm_config.get_llm_models()

        if not model:
            st.error("Failed to initialize the LLM model. Please check your configuration.")
            return {}

        graph_builder = GraphBuilder(model)
        try:
            graph = graph_builder.setup_graph(usecase)
        except Exception as e:
            st.error(f"Error setting up graph: {e}")
            with st.expander("Graph setup trace", expanded=True):
                st.text(traceback.format_exc())
            return {}

        # Display/stream results using the DisplayResultStreamlit component
        display_result = DisplayResultStreamlit(usecase, graph)
        display_result.display_result_on_ui(user_message)

    except Exception as e:
        st.error(f"Error initializing or running LLM/graph: {e}")
        with st.expander("Initialization error (trace)", expanded=True):
            st.text(traceback.format_exc())
        return {}

    return user_controls


if __name__ == "__main__":
    load_langgraph_agenticai_app()
