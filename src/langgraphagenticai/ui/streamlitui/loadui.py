# loadui.py
import streamlit as st
from src.langgraphagenticai.ui.uiconfigfile import Config
import os

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls: dict = {}

        # ensure session keys exist (so text_input preserves value)
        if "GROQ_API_KEY" not in st.session_state:
            st.session_state["GROQ_API_KEY"] = ""
        if "user_input" not in st.session_state:
            st.session_state["user_input"] = ""
        if "run_count" not in st.session_state:
            st.session_state["run_count"] = 0

    def load_streamlit_ui(self) -> dict:
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        st.session_state.timeframe = ""
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            st.header("Configuration")

            # LLM selection (read options from Config)
            llm_options = self.config.get_llm_options()
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            # Groq-specific settings
            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Groq Model", model_options)

                # Persist API key in session_state so it survives reruns
                st.session_state["GROQ_API_KEY"] = st.text_input(
                    "Groq API Key", value=st.session_state.get("GROQ_API_KEY", ""), type="password"
                )
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Get one from Groq Console if needed.")
            else:
                # ensure keys are present but empty
                self.user_controls.setdefault("selected_groq_model", None)
                self.user_controls.setdefault("GROQ_API_KEY", "")

            st.markdown("---")
            # Use-case selection (read options from Config)
            usecase_options = self.config.get_usecase_options()
            self.user_controls["selected_usecase"] = st.selectbox("Select Use Case", usecase_options)

            if self.user_controls["selected_usecase"] is None:
                st.warning("⚠️ Please select a use case to proceed.")
                
            if self.user_controls["selected_usecase"] == "Chatbot with Tool" or self.user_controls["selected_usecase"] == "AI News":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API KEY", type="password")
        
        
        if self.user_controls['selected_usecase']== "AI News":
            st.subheader("📰 AI News")
            
            with st.sidebar:
                time_frame = st.selectbox(
                "Select Time Frame for News:",
                options=["Past Day", "Past Week", "Past Month", "Past Year"],
                index=0
                )
                if st.button("Fetch latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame
        
        return self.user_controls
