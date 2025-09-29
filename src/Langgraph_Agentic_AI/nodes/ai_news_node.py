from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import os


class AINewsNode:
    def __init__(self, llm):
        """
        Initialize the AINewsNode with API keys for Tavily and GROQ.
        """
        self.tavily = TavilyClient()
        self.llm = llm
        ## this is used to capture various steps i this file so that later can be use for stops shown
        self.state = {}
    
    def fetch_news(self, state: dict)-> dict:
        """
        Fetch Ai news based on the specified frequency.
        
        Args:
        state (dict) : THe state dictionary containing 'frequency'.
        
        Returns:
            dict: upload state with 'news_data' key containing fetched news.
        """
        
        frequency = state["messages"][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {'daily':'d','weekly':'w','monthly':'m','yearly':'y'}
        days_map = {'daily':1,'weekly':7,'monthly':30,'yearly':365}
        
        response = self.tavily.search(
            query="Top Artificial Intelligenece(AI) technology news india and globally",
            topic = "news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days = days_map[frequency],
            # include_domains = ['techcrunch.com','venturebeat.com/ai',....] 
        )
        
        state['news_data'] = response.get('results',[])
        self.state['news_data'] = state['news_data']
        
        return state
    def summarize_news(self, state:dict) -> dict:
        """
        Summarize the fetched news using an LLm.
        
        Args:
        state (dict): The state dictionary containing 'news_data.
        
        Returns:
        dict: Updated state with 'summary' key containing the summarized news.
        """
        
        news_items = self.state['news_data']
        prompt_template = ChatPromptTemplate.from_messages([
            ("system","""Summarize AI news article into markdown format. for each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise( Latest first)
            - Source URL as link
            Use Format:
            ### [Date]
            
            - [Summary](URL)"""),
            ("user","Articles:\n{articles}")
        ])
        
        articles_str = "\n\n".join([
            f"Content: {item.get('content','')}\nURL: {item.get('url','')}\nDate: {item.get('published_date','')}"
            for item in news_items
        ])
        
        response = self.llm.invoke(prompt_template.format(articles = articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return state
    
    def save_result(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        
        # Create AINews directory if it doesn't exist
        os.makedirs("./AINews", exist_ok=True)
        
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
            
        self.state['filename'] = filename
        state['filename'] = filename
        return state