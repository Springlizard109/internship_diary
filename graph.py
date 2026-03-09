from langgraph.graph import StateGraph
from typing import TypedDict
from rag_pipeline import retrieve_docs


class GraphState(TypedDict):
    question: str
    documents: list
    answer: str


def retrieve(state):

    docs = retrieve_docs(state["question"])

    return {"documents": docs}


from langchain_ollama import ChatOllama

llm = ChatOllama(model="phi3")


def generate(state):
    
    docs = state["documents"]
    question = state["question"]

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {"answer": response.content}


def build_graph():


    workflow = StateGraph(GraphState)

    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)

    workflow.set_entry_point("retrieve")

    workflow.add_edge("retrieve", "generate")

    return workflow.compile()

from langchain_ollama import ChatOllama

llm = ChatOllama(model="phi3")

def analyze_query(state):

    question = state["question"]

    prompt = f"""
Decide if the following question requires retrieving documents
from a knowledge base.

Answer only with:
YES
or
NO

Question: {question}
"""

    response = llm.invoke(prompt)

    decision = response.content.strip()

    return {"decision": decision}

def route_query(state):
    
    if "YES" in state["decision"]:
        return "retrieve"
    else:
        return "direct_answer"
    
def direct_answer(state):
    
    question = state["question"]

    response = llm.invoke(question)

    return {"answer": response.content}

def build_graph():
    
    workflow = StateGraph(GraphState)

    workflow.add_node("analyze", analyze_query)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)
    workflow.add_node("direct_answer", direct_answer)
    workflow.add_node("evaluate", evaluate_answer)

    workflow.set_entry_point("analyze")

    workflow.add_conditional_edges(
        "analyze",
        route_query,
        {
            "retrieve": "retrieve",
            "direct_answer": "direct_answer"
        }
    )

    workflow.add_edge("retrieve", "generate")
    
    workflow.add_edge("generate", "evaluate")
    
    workflow.add_conditional_edges(
    "evaluate",
    route_evaluation,
    {
        "retrieve": "retrieve",
        "end": "__end__"
    }
)

    return workflow.compile()

def evaluate_answer(state):
    
    question = state["question"]
    answer = state["answer"]
    docs = state["documents"]

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
Check if the answer is supported by the context.

Context:
{context}

Question:
{question}

Answer:
{answer}

Reply only with:
GOOD
or
BAD
"""

    response = llm.invoke(prompt)

    return {"evaluation": response.content.strip()}

class GraphState(TypedDict):
    question: str
    documents: list
    answer: str
    decision: str
    evaluation: str
    
def route_evaluation(state):
    
    if "GOOD" in state["evaluation"]:
        return "end"
    else:
        return "retrieve"