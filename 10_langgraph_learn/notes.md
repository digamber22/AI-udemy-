# LangGraph Notes

## 1) What is LangGraph?

LangGraph is a low-level orchestration framework and runtime for building stateful, long-running agent workflows. It is designed for durable execution, streaming, human-in-the-loop control, and memory. The Graph API is centered on nodes, edges, and shared state, so you can represent an LLM app as a graph instead of a long chain of nested if/elif logic. In simple words, LangGraph helps you control what happens next in an AI app, especially when the app has multiple steps, loops, branches, tool calls, approvals, retries, or different paths based on the current state.

## 2) What problems does it solve?

Traditional Python code for complex AI workflows often becomes messy when you keep adding many if, elif, else, retries, loops, and special cases. LangGraph solves this by turning the workflow into a graph where each decision is explicit and each step is separated into a node. That makes branching logic clearer, easier to debug, and easier to extend. It is especially useful for complex decision trees, multi-step agents, loops and retries, tool-using assistants, human review steps, workflows that need to pause and resume, and cases where you want to preserve state across steps.

## 3) Why not just use many if and elif conditions?

A big if/elif chain works for small logic, but it becomes hard to read when the app grows. For example:

```python
if user_intent == "billing":
    ...
elif user_intent == "tech":
    ...
elif user_intent == "refund":
    ...
elif user_intent == "human_help":
    ...
else:
    ...
```

LangGraph replaces this kind of branching with a routing function and conditional edges. Instead of hiding the logic inside one long function, each branch becomes its own node, and the router decides the next node from the current state. That makes the flow easier to visualize and maintain.

## 4) Main concepts

**State**: State is the shared data of the graph. It is the current snapshot of the application and is commonly defined with TypedDict, Pydantic, or a dataclass. Nodes read the state and return updates to it.

**Node**: A node is just a Python function. It receives the current state, does some work, and returns a partial or full state update. Nodes can be synchronous or asynchronous. LangGraph also turns functions into runnable objects behind the scenes.

**Edge**: An edge connects one node to another. Normal edges mean “go directly to the next node.” Edges are how the graph decides the route of execution.

**Conditional edge**: A conditional edge uses a routing function to decide which node to go to next based on the current state. This is the key feature that replaces many if/elif branches. The routing function can return one node, several nodes, or a mapping like True -> node_b, False -> node_c.

**START and END**: START is the virtual entry point of the graph, and END is the terminal node. You use them to define where execution begins and where it stops.

**StateGraph / graph builder**: StateGraph is the main graph-building class. You define state, add nodes, add edges, and then compile the graph. In practice, StateGraph(...) is the builder object.

**Compile**: After building the graph, you call .compile(). Compilation performs checks on the graph structure and prepares it for execution.

**Invoke**: After compiling, you run the graph with .invoke(...). In the quickstart, the graph is invoked with an initial input like {"messages": [...]}. LangGraph also supports streaming with .stream(...).

**Reducer**: A reducer defines how a state field is updated when multiple updates happen. This matters when the graph accumulates messages or combines updates over time.

**MessagesState**: Because message lists are common in LLM apps, LangGraph provides MessagesState, which already includes a messages field and message-reduction behavior.

**Command**: Command is a control primitive that can both update state and route to another node in one step. It is useful when you want to combine state update and navigation together.

**Send**: Send is useful for patterns like map-reduce, where one node produces many items and you want to send different state to multiple downstream nodes.

**Subgraphs**: Subgraphs let you nest one graph inside another. This is useful when a part of the workflow should be isolated or reused.
#
## Checkpointing in LangGraph (Short Notes)

### What is Checkpointing?
Checkpointing is the process of **saving the state of a LangGraph workflow at every step** so it can be reused later.

## Why it is Important?
- Provides **memory** to the agent  
- Allows **continuation of conversation**  
- Helps in **debugging and recovery**  
- Supports **long-running workflows**

### Without Checkpointing
- State is **not saved**
- Every run starts **fresh**
- Example:
  - Input: "My name is Digamber"
  - Next query: "What is my name?"
  - ❌ Agent cannot answer (no memory)

### With Checkpointing
- State is **saved after each step**
- Agent can **remember previous inputs**
- Example:
  - Input: "My name is Digamber"
  - Next query: "What is my name?"
  - ✅ Output: "Digamber"

### Using MongoDB for Checkpointing
MongoDB can be used to **store the state (checkpoints)**.

### Steps:
1. Connect to MongoDB  
2. Create a checkpointer (`MongoDBSaver`)  
3. Compile graph with checkpointer  
4. Use same `thread_id` to continue state  

### Key Concept
- **Thread ID** → Identifies a conversation  
- **Checkpoint** → Saved state of that thread  
- **State** → Data shared between nodes  

### One Line Summary
Checkpointing = **Saving state at every step so the agent does not forget.**

#
## 5) How LangGraph works, step by step

First, you define the state schema. This tells LangGraph what data the graph will carry. Then you create nodes as functions that read state and return updates. After that, you connect nodes using edges or conditional edges. Once the structure is ready, you compile the graph, and then you invoke it with the initial input. Execution proceeds step by step until the graph reaches END or no more active nodes remain. The important idea is that LangGraph treats workflow as a stateful process. Each node updates the shared state, and edges decide where control goes next. That is why it fits agent workflows, tool loops, branching logic, and review cycles very well.

## 6) Example: replacing many if/elif conditions

Imagine a support chatbot that needs to route a user message into one of several paths: billing issue, technical issue, refund request, human review, or general answer. Instead of writing one huge function with many branches, you can make one router node and separate nodes for each path. The router inspects the current state and returns the next node name through a conditional edge. This keeps each responsibility separate and much easier to manage.

Flow:

`START -> classify_intent -> [billing_node / tech_node / refund_node / human_review_node / general_node] -> END`

This is exactly the kind of workflow LangGraph is built for: explicit branching, shared state, and clear control flow.

### Sample code

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message: str
    intent: str
    answer: str

def classify_intent(state: State):
    text = state["message"].lower()

    if "refund" in text:
        return {"intent": "refund"}
    elif "bill" in text or "payment" in text:
        return {"intent": "billing"}
    elif "error" in text or "bug" in text:
        return {"intent": "tech"}
    else:
        return {"intent": "general"}

def refund_node(state: State):
    return {"answer": "I will help you with the refund process."}

def billing_node(state: State):
    return {"answer": "I will help you with the billing issue."}

def tech_node(state: State):
    return {"answer": "I will help you with the technical issue."}

def general_node(state: State):
    return {"answer": "I will help you with your question."}

def route_next(state: State):
    return state["intent"]

builder = StateGraph(State)

builder.add_node("classify_intent", classify_intent)
builder.add_node("refund_node", refund_node)
builder.add_node("billing_node", billing_node)
builder.add_node("tech_node", tech_node)
builder.add_node("general_node", general_node)

builder.add_edge(START, "classify_intent")
builder.add_conditional_edges(
    "classify_intent",
    route_next,
    {
        "refund": "refund_node",
        "billing": "billing_node",
        "tech": "tech_node",
        "general": "general_node",
    }
)

builder.add_edge("refund_node", END)
builder.add_edge("billing_node", END)
builder.add_edge("tech_node", END)
builder.add_edge("general_node", END)

graph = builder.compile()

result = graph.invoke({"message": "I need a refund", "intent": "", "answer": ""})
print(result)
```

This example shows the main pattern: the graph stores state, nodes modify that state, and conditional edges decide the next path. That is the clean LangGraph alternative to a long if/elif chain.

## 7) Why this is better for complex AI apps

LangGraph becomes very helpful when your app is no longer a straight line. For example, an agent may ask a model to classify the user request, decide whether to call a tool, wait for human approval, retry on failure, branch into different workflows, or resume later from saved state. LangGraph supports these patterns with graphs, state, conditional branching, interrupts, persistence, streaming, and subgraphs.

## 8) Simple mental model

Think of LangGraph like this: State = notebook of what the app currently knows, Node = one step of work, Edge = connector between steps, Conditional edge = if/elif logic turned into routing, Graph builder = place where you assemble the workflow, Compile = finalize the workflow, Invoke = start the workflow with input. That mental model is enough to understand most LangGraph apps.

## 9) One-line summary

LangGraph is a way to build AI workflows as a stateful graph of functions, so complex branching, loops, tool use, and multi-step logic stay organized instead of turning into a huge if/elif mess.
