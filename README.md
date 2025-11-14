# Agentic AI Chatbot Project

## 📒 Index

- [Project Overview](#-project-overview)  
- [Tech Stack](#-tech-stack)  
- [Key Learnings](#-key-learnings)  
- [Getting Started](#-getting-started)  
- [Contribution & Support](#-contribution--support)  

***

## 🚀 Project Overview

This project features an end-to-end **Agentic AI Chatbot** with three key modules:

1. **Basic Chatbot**  
   A conversational agent powered by a large language model (LLM) to handle general user queries.

2. **Chatbot with Tavily Tool**  
   An extension integrating the Tavily API to perform real-time web searches and tool calls, enriching the chatbot's responses.

3. **AI News Generator**  
   Fetches and summarizes AI news across selectable time frames — past day, week, month, or year — leveraging Tavily's data and LLM summarization.

Users can dynamically switch between modules in a unified interface.

***

## 🛠️ Tech Stack

- **Backend & AI**  
  - GroqLLM: Advanced LLM model for chat intelligence  
  - LangGraph: Agentic AI orchestration and stateful workflow management  
  - Langchain Core: Prompt templates and message handling  
  - Tavily API: Real-time web data retrieval and search tool  

- **Frontend & UI**  
  - Streamlit: Interactive web application framework delivering seamless chatbot UI  

- **Supporting Technologies**  
  - Python 3.x  
  - Markdown & JSON formatting for content  
  - Git for version control  

***

## 📝 Key Learnings

- Modular chatbot design aids flexibility and code maintainability.  
- Stateful conversation graphs unlock sophisticated multi-turn dialog management.  
- Proper handling of streamed AI output is critical for responsive UX.  
- Robust error handling ensures resiliency against incomplete or failed API responses.  
- Unicode and encoding nuances must be managed carefully when dealing with diverse content sources.  
- Dynamic prompt crafting improves AI summarization relevance and quality.  
- Visibility into raw backend data via debug outputs accelerates troubleshooting.

***

## 💻 Getting Started

### Prerequisites

- Python 3.8 or higher  
- Valid Groq and Tavily API keys  
- Familiarity with Streamlit and basic Python  

### Installation & Run

```bash
git clone https://github.com/AKAK555/Agentic-Chatbot.git
cd Agentic-Chatbot
pip install -r requirements.txt
streamlit run src/langgraphagenticai/main.py
```

### Configuration

- Provide Groq and Tavily API keys in the sidebar input fields.  
- Select your desired chatbot module and news time frame as applicable.

***

## 🤝 Contribution & Support

Contributions and feedback are welcome! Please create issues or pull requests on GitHub.

Thank you for exploring the Agentic AI Chatbot project — combining modern AI workflows and dynamic data integration to deliver a powerful conversational experience.
