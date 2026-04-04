 # “Replace hardcoded evaluation with an AI call to check if response is good or not (minimal changes).

from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}

def samplenode(state: State):
    print("\n\nInside samplenode node", state)

    # hardcoded response
    hardcoded_response = AIMessage(content="Sample Message Appended")
    return {"messages": [hardcoded_response]}

def evaluate_node(state: State):
    last_msg = state["messages"][-1].content

    prompt = f"""
    Evaluate this response:
    "{last_msg}"

    Reply only with:
    GOOD - if it is correct/useful
    BAD - if it is not
    Add one short reason.
    """

    evaluation = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [evaluation]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)
graph_builder.add_node("evaluate_node", evaluate_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", "evaluate_node")
graph_builder.add_edge("evaluate_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": [HumanMessage(content="What is my name?")]}))
print("\n\nupdated_state", updated_state)