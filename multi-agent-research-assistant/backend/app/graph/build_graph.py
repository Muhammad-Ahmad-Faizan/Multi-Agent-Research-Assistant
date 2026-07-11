from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.graph.state import ResearchState
from app.graph.nodes import planner_node, researcher_node, analyzer_node, writer_node
from app.config import settings

def should_continue_research(state: ResearchState):
    plan = state.get("plan", [])
    idx = state.get("current_subquestion_index", 0)
    if idx < len(plan):
        return "researcher"
    return "analyzer"

def should_loop_back(state: ResearchState):
    needs_more = state.get("needs_more_research", False)
    # The max loop check is already handled in the analyzer_node (it forces needs_more to False)
    # but we can double check here.
    if needs_more:
        return "researcher"
    return "writer"

def build_graph(interrupt=False):
    builder = StateGraph(ResearchState)
    
    builder.add_node("planner", planner_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("analyzer", analyzer_node)
    builder.add_node("writer", writer_node)
    
    builder.set_entry_point("planner")
    
    builder.add_edge("planner", "researcher")
    
    builder.add_conditional_edges(
        "researcher",
        should_continue_research,
        {
            "researcher": "researcher",
            "analyzer": "analyzer"
        }
    )
    
    builder.add_conditional_edges(
        "analyzer",
        should_loop_back,
        {
            "researcher": "researcher",
            "writer": "writer"
        }
    )
    
    builder.add_edge("writer", END)
    
    memory = MemorySaver()
    
    if interrupt:
        graph = builder.compile(checkpointer=memory, interrupt_after=["planner"])
    else:
        graph = builder.compile(checkpointer=memory)
    
    return graph
