from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate



class AINewsNode:
    """
    AI News Generator Node:
    - Fetches news articles using Tavily API
    - Summarizes the fetched news using the provided LLM
    - Returns summarized news content
    """

    def __init__(self, llm):
        self.tavily = TavilyClient()
        self.llm = llm
        
        self.state = {}
        
    def fetch_news(self, state: dict)-> dict:
        """Fetch AI News based on specified frequency."""
        
        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {
            'past day': 'd',
            'past week': 'w',
            'past month': 'm',
            'past year': 'y'
        }

        days_map = {
            'past day': 1,
            'past week': 7,
            'past month': 30,
            'past year': 366
        }

        response = self.tavily.search(
            query="Top AI Tech News both India and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days=days_map[frequency],
        )

        if not response or not isinstance(response, dict):
            # Handle gracefully by assigning empty list or logging warning
            state['news_data'] = []
            self.state['news_data'] = []
        else:
            state['news_data'] = response.get('results', [])
            self.state['news_data'] = state['news_data']

        
        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state
    
    
    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using an LLM.
        
        Args:
            state (dict): The state dictionary containing 'news_data'.
        
        Returns:
            dict: Updated state with 'summary' key containing the summarized news.
        """

        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state
    
    def save_result(self,state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state