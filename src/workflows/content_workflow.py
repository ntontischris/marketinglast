from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from src.agents.core.content_strategy import ContentStrategyAgent

# Define the state for our workflow
class AgentState(TypedDict):
    """Represents the state of our workflow.
    
    Attributes:
        topic: The input topic for content generation.
        ideas: The generated content ideas.
    """
    topic: str
    ideas: Optional[str]

def create_content_workflow():
    """Creates and compiles the content generation workflow graph."""
    print("--- CREATING CONTENT WORKFLOW ---")
    
    # Initialize the agent
    content_strategist = ContentStrategyAgent()

    # Create a new state graph
    workflow = StateGraph(AgentState)

    # Add the content strategist as a node in the graph
    workflow.add_node("strategist", content_strategist)

    # The graph starts at the 'strategist' node
    workflow.set_entry_point("strategist")

    # The graph ends after the 'strategist' node has run
    workflow.add_edge("strategist", END)

    # Compile the graph into a runnable app
    app = workflow.compile()
    
    print("--- CONTENT WORKFLOW CREATED AND COMPILED ---")
    return app
