from langgraph.graph import StateGraph, START, END
from src.Langgraph_Agentic_AI.nodes.basic_chatbot_node import BasicChatBotNode
from src.Langgraph_Agentic_AI.state.state import State
from src.Langgraph_Agentic_AI.tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import ToolNode,tools_condition
from src.Langgraph_Agentic_AI.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.Langgraph_Agentic_AI.nodes.ai_news_node import AINewsNode


class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot node using LangGraph.
        This method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrate it into the graph. The chatbot node is set as both the
        entry and exit point of the graph.
        """
        self.basic_chatbot_node = BasicChatBotNode(self.llm)
        
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot",END)
       
    def chatbot_with_tools_build_graph(self):
        """
            Builds an advanced chatbot with tool integration.
            This method creates a chatbot graph that includes both a chatbot node and a tool node. It defines tools, initializes the chatbot with tool capabilities, and sets up conditional and direct edges between nodes.
            The chatbot node is set as the entry point.
        """ 
        ## Defining the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)
        
        ## define the llm
        llm = self.llm
        
        # Define the chatbot node
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)
        
        ## add the node
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        
    def ai_news_builder_graph(self):
        
        # AI news node
        ai_news_node = AINewsNode(self.llm)
        
        
        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("Summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_news_node.save_result)
        
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "Summarize_news")
        self.graph_builder.add_edge("Summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)
        
    def setup_graph(self, usecase: str):
        """
        Sets up the graph for thr selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
                    
        if usecase == "Chatbot with Web":
            self.chatbot_with_tools_build_graph()
            
        if usecase == "AI News":
            self.ai_news_builder_graph()
             
        return self.graph_builder.compile()
