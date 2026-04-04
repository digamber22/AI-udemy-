from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

# initialize llm model
llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)

# simple state of messages 
class State(TypedDict):
    messages: Annotated[list, add_messages]

# llm invocation 
def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return { "messages": [response] }

def samplenode(state: State):
    print("\n\nInside samplenode node", state)
    return { "messages": ["Sample Message Appended"] }

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["What is my name?"]}))   # for running the code give initial message 
print("\n\nupdated_state", updated_state)

# (START) -> chatbot -> samplenode -> (END)    # two nodes (e.g chatbot, samplenode) and three edges (e.g b/w start to chatbot, c & s , s and end )

# state = { messages: ["Hey there"] }
# node runs: chatbot(state: ["Hey There"]) -> ["Hi, This is a message from ChatBot Node"]
# state = { "messages": ["Hey there", "Hi, This is a message from ChatBot Node"]  }