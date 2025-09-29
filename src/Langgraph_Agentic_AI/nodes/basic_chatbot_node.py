from src.Langgraph_Agentic_AI.state.state import State
class BasicChatBotNode:
    """
    This is basic chatbot login implementation.
    """
    
    def __init__(self,model):
        self.llm = model
    
    def process(self, state: State) -> dict:
        """
        Process the input strucutre of the state used in graph
        """
        
        return {"messages":self.llm.invoke(state['messages'])}