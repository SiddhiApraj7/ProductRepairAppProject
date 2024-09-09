from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph
from agents import web_search, transform_query, generate, retrieve_info, router

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: product repair problem to be fixed with its details
        search_query: transformed query to search web or db
        context: relevant useful information gathered from domain-specific database or via the internet
        generation: final answer/procedure generation
    """
    question : str
    search_query : str
    context : str
    generation : str
    

# Build the nodes
workflow = StateGraph(GraphState)
workflow.add_node("websearch", web_search)
workflow.add_node("transform_query", transform_query)
workflow.add_node("generate", generate)
workflow.add_node("retrieve", retrieve_info)

# Build the edges
workflow.set_entry_point("transform_query")
workflow.add_edge("transform_query", "retrieve")
workflow.add_conditional_edges(
    "retrieve",
    router,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)
workflow.add_edge("websearch", "generate")
workflow.add_edge("generate", END)

# Compile the workflow
complete_agent = workflow.compile()

def run_complete_agent(query):
    dictionary = {
        "question": query,
        "context": None
    }
    #print(dictionary)
    output = complete_agent.invoke(dictionary)
    return output