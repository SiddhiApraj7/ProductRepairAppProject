from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.chat_models import ChatOllama
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from vector_db_load import vector_db_instance
import logging

local_llm = 'llama3.1'
llama3 = ChatOllama(model=local_llm, temperature=0)
llama3_json = ChatOllama(model=local_llm, format='json', temperature=0)

wrapper = DuckDuckGoSearchAPIWrapper(max_results=25)
web_search_tool = DuckDuckGoSearchRun(api_wrapper=wrapper)

vector_db = vector_db_instance

# transform query
search_query_prompt = PromptTemplate(
    template="""
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|> 
    
    You are an expert at crafting web search/db search queries for product repair questions.
    More often than not, a user will ask for help to solve an issue they are facing with a product, however it might not be in the best format. 
    Reword their query to be the most effective web search/database search string possible.
    Return the JSON with a single key 'query' with no premable or explanation. 
    
    Question to transform: {question} 
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>
    """,
    input_variables=["question"],
)

search_query_chain = search_query_prompt | llama3_json | JsonOutputParser()


# rag
rag_query_prompt = PromptTemplate(
    template="""
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|> 
    
    You are an expert at generating 3 different versions of a given user product repair questions to retrieve relevant documents from a vector database.
    By generating multiple perspectives on the user question, your
    goal is to help the user overcome some of the limitations of the distance-based
    similarity search. Provide these alternative questions separated by newlines.
        
    Original question: {question} 
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>
    """,
    input_variables=["question"],
)


# generation 
generate_prompt = PromptTemplate(
    template="""
    
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|> 
    
    You are an AI assistant for Product Repair Tasks, that synthesizes results obtained from domain-specific databse or web searches. 
    Strictly use the following pieces of context to answer the question. If you don't know the answer, just say that you don't know. 
    keep the answer concise, but provide all of the details you can in the form of concise actionable steps. 
    You need to help the user fix their product with your help.
    Only make direct references to material if provided in the context.
    
    <|eot_id|>
    
    <|start_header_id|>user<|end_header_id|>
    
    Question: {question} 
    Context: {context} 
    Answer: 
    
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "context"],
)

generate_chain = generate_prompt | llama3 | StrOutputParser()


# functions

def transform_query(state):
    """
    Transform user question to web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended search query
    """
    
    print("Step: Optimizing Query for Web Search")
    question = state['question']
    gen_query = search_query_chain.invoke({"question": question})
    search_query = gen_query["query"]
    return {"search_query": search_query}


def web_search(state):
    """
    Web search based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to context
    """

    print(state)
    search_query = state['search_query']
    print(f'Step: Searching the Web for: "{search_query}"')
    
    search_result = web_search_tool.invoke(search_query)
    return {"context": search_result}



def retrieve_info(state):
    
    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), 
        llama3,
        prompt=rag_query_prompt
    )
    
    logging.basicConfig()
    logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)
    context = retriever.invoke(state['search_query'])
    print(len(context))
    
    template = """Check if the ONLY the provided context is sufficent to answer the provided question:
    {context}
    Question: {question}
    If you have no relevant context(I mean the info you have is not for specific product or you have no relevant info in context), simply respond with 'I don't know.' only and nothing else.
    If the context is relevant, reply only with "Relevant." and nothing else.'
    """
    
    #prompt = ChatPromptTemplate.from_template(template)
    search_query = state['search_query']
    #context = retriever.retriever(search_query)
    
    formatted_prompt = template.format(context=context, question=search_query)
    info = llama3.invoke(formatted_prompt)
    
    if info.content == "Relevant.":
        print("Context relevant, Generation")
        return {
        "search_query": search_query, 
        "context": context
        }
    elif info.content == "I don't know.":
        print("Context irrelevant, Search")
        return {
        "search_query": search_query, 
        "context": info.content
        }


def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    
    print("Step: Generating Final Response")
    question = state["question"]
    context = state["context"]

    generation = generate_chain.invoke({"context": context, "question": question})
    return {"generation": generation}


def router(state):
    print(state)
    """
    route to web search or generation.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("Step: Routing Query")
    #question = state['question']
    #output = question_router.invoke({"question": question})
    if state["context"] == "I don't know.":
        print("Step: Routing Query to Web Search")
        return "websearch"
    else:
        print("Step: Routing Query to Generation")
        return "generate"