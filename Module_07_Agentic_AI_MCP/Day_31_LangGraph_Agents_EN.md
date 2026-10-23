# Day 31: Multi-Agent Systems & LangGraph (State, Nodes, Edges & Human-in-the-Loop) 🕸️

---

## 1. Day 31 Learning Objectives
- Understand why stateful directed graphs (**LangGraph**) supersede rigid, linear chains for production AI agents.
- Master core LangGraph primitives: **State (TypedDict / Pydantic)**, **Nodes (Python functions)**, **Edges (normal & conditional)**, and **Checkpointers (persistence)**.
- Implement **Human-in-the-Loop (HITL)** workflows where agents interrupt execution before taking high-risk actions (e.g., executing financial transfers, sending emails, deleting records).
- Build multi-agent coordination architectures: Supervisor pattern vs. Hierarchical teams.
- Handle state rollbacks, retry mechanisms, and sub-graph isolation.

---

## 2. Real-World Analogy

> 💡 **Analogy: Assembly Line vs. Emergency Room Workflow**
>
> - **Linear Chain (LangChain / Sequential):** Think of an automated soda bottling line. Bottle enters -> wash -> fill -> cap -> label -> exit. If the bottle is cracked at step 2, the machine still tries to pour soda and cap it, making a giant mess. It cannot go backwards or decide to route the bottle to an inspector.
> - **Stateful Graph (LangGraph):** Think of an **Emergency Room (ER)** in a hospital!
>   - **State:** The patient's chart (vitals, symptoms, doctor's notes, test results).
>   - **Triage Nurse (Node 1):** Checks vitals. If heart rate is dangerously high, routes via a **Conditional Edge** immediately to the **Cardiology Specialist (Node 2)**.
>   - **Cardiologist (Node 2):** Orders an ECG. State is updated with ECG results.
>   - **Human-in-the-Loop (Interrupt):** Before administering high-risk medication, the system **pauses** and demands: *"Senior Doctor signature required to proceed."*
>   - Once signed, execution resumes seamlessly right where it paused!

---

## 3. Architecture Overview: LangGraph Workflow

```
                                 ┌──────────────┐
                                 │  START NODE  │
                                 └──────┬───────┘
                                        │
                                        ▼
                            ┌───────────────────────┐
                            │      Supervisor       │
                            │  (Evaluates Request)  │
                            └───────────┬───────────┘
                                        │
                         Conditional Routing (router_edge)
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
             ┌─────────────────────┐         ┌─────────────────────┐
             │    Coder Agent      │         │   Researcher Agent  │
             │ (Generates Code)    │         │ (Fetches Web Info)  │
             └──────────┬──────────┘         └──────────┬──────────┘
                        │                               │
                        └───────────────┬───────────────┘
                                        ▼
                            ┌───────────────────────┐
                            │    Code Reviewer      │
                            │  (Tests & Validates)  │
                            └───────────┬───────────┘
                                        │
                       Did tests pass?  │
                      ┌─────────────────┴─────────────────┐
                      │ No                                │ Yes
                      ▼                                   ▼
        [Loop back to Coder Node]              ┌─────────────────────┐
                                               │   HUMAN APPROVAL    │
                                               │   (HITL Pause)      │
                                               └──────────┬──────────┘
                                                          │ Approved
                                                          ▼
                                               ┌─────────────────────┐
                                               │      END NODE       │
                                               └─────────────────────┘
```

---

## 4. Key Primitives of LangGraph

1. **State:** The shared memory / data contract that flows through every node. In Python, typically modeled with `TypedDict` or Pydantic, using `Annotated` reducers like `add_messages` to append instead of overwrite conversation turns.
2. **Nodes:** Plain Python functions that receive the current State as input, perform work (call LLM, query DB, execute code), and return a dictionary containing updated state keys.
3. **Edges:** Direct the flow from one node to the next.
   - *Normal Edge (`add_edge`):* Node A always goes to Node B.
   - *Conditional Edge (`add_conditional_edges`):* A router function inspects the state and returns the name of the next node or `END`.
4. **Memory & Checkpointing:** Saves state snapshots at every step into memory, SQLite, or PostgreSQL, enabling time-travel, pausing, resuming, and audit trails.

---

## 5. Coding Walkthrough: Building an Agent with LangGraph & HITL

Let's build a functional, fully typed LangGraph workflow showcasing Nodes, Conditional Edges, and Human Approval using clean Python:

```python
import operator
from typing import Annotated, TypedDict, Literal, List
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

# 1. Define Agent State (The data contract)
class AgentState(TypedDict):
    task: str
    code: str
    test_passed: bool
    iterations: int
    human_approved: bool
    logs: Annotated[List[str], operator.add]  # Appends logs rather than overwriting

# 2. Define Worker Nodes (Plain Python Functions)
def developer_node(state: AgentState) -> dict:
    """Generates or fixes Python code."""
    iteration = state.get("iterations", 0) + 1
    task = state["task"]
    
    if iteration == 1:
        # First attempt: intentionally buggy code
        code = "def add(a, b):\n    return a - b  # Buggy implementation"
        log = "Developer wrote initial draft (with intentional bug)."
    else:
        # Second attempt: fixed code
        code = "def add(a, b):\n    return a + b  # Fixed implementation"
        log = "Developer reviewed error and resolved addition bug."
        
    return {
        "code": code,
        "iterations": iteration,
        "logs": [log]
    }

def test_runner_node(state: AgentState) -> dict:
    """Executes unit tests against the generated code."""
    code = state["code"]
    
    # Execute code in safe sandbox (mocked test)
    namespace = {}
    try:
        exec(code, namespace)
        add_fn = namespace["add"]
        assert add_fn(2, 3) == 5, "Test failed: add(2, 3) != 5"
        return {
            "test_passed": True,
            "logs": ["TestRunner: All unit tests PASSED ✅"]
        }
    except Exception as e:
        return {
            "test_passed": False,
            "logs": [f"TestRunner: Unit test FAILED with error: {str(e)} ❌"]
        }

def deploy_node(state: AgentState) -> dict:
    """Production deployment node."""
    return {
        "logs": [f"DeployNode: Deployed verified code to production 🚀: \n{state['code']}"]
    }

# 3. Define Conditional Routing Function
def routing_logic(state: AgentState) -> Literal["developer", "human_approval", "__end__"]:
    """Decides where to go based on test status and retry limits."""
    if state["test_passed"]:
        return "human_approval"
    
    if state["iterations"] >= 3:
        return "__end__"  # Circuit breaker: stop looping if failing continuously
    
    return "developer"  # Loop back to developer to fix code

# 4. Assemble the StateGraph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("developer", developer_node)
workflow.add_node("test_runner", test_runner_node)
workflow.add_node("deploy", deploy_node)

# Add Edges
workflow.add_edge(START, "developer")
workflow.add_edge("developer", "test_runner")

# Conditional Edge from test_runner
workflow.add_conditional_edges(
    "test_runner",
    routing_logic,
    {
        "developer": "developer",
        "human_approval": "deploy",  # Will pause before entering deploy
        "__end__": END
    }
)
workflow.add_edge("deploy", END)

# 5. Compile with Checkpointing and Interrupt (Human-in-the-Loop)
memory = MemorySaver()
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["deploy"]  # ⏸️ PAUSE execution before deploying to production!
)

# 6. Execution Simulation
if __name__ == "__main__":
    thread_config = {"configurable": {"thread_id": "session-101"}}
    
    initial_input = {
        "task": "Create an addition function",
        "code": "",
        "test_passed": False,
        "iterations": 0,
        "human_approved": False,
        "logs": ["Workflow started."]
    }
    
    print("\n--- Phase 1: Running Graph Until Human-In-The-Loop Pause ---")
    for event in app.stream(initial_input, config=thread_config):
        for node_name, output in event.items():
            print(f"[{node_name}] -> {output.get('logs', [''])[0]}")
            
    # Inspect current state when interrupted
    snapshot = app.get_state(thread_config)
    print("\n⏸️ GRAPH HAS PAUSED!")
    print(f"Next scheduled node: {snapshot.next}")
    print(f"Current verified code:\n{snapshot.values['code']}")
    
    # Simulate Human Review
    human_choice = "approve"  # Simulating human typing 'approve'
    if human_choice == "approve":
        print("\n--- Phase 2: Human Approved! Resuming Execution ---")
        for event in app.stream(None, config=thread_config):
            for node_name, output in event.items():
                print(f"[{node_name}] -> {output.get('logs', [''])[0]}")
```

---

## 6. Common Fresher Pitfalls

| Pitfall | Why It Breaks | How to Avoid (Best Practice) |
| :--- | :--- | :--- |
| **Overwriting State Lists** | Defining `logs: List[str]` without a reducer causes each node to replace the entire list with only its own logs. | Always use `Annotated[List[str], operator.add]` so each node appends cleanly to history. |
| **Infinite Graph Cycles** | If an LLM keeps generating failing code or a conditional edge condition is never met, the graph loops forever, burning API credits. | Always include an `iteration_count` variable in state and a circuit breaker (`if iterations >= max_retries: return END`). |
| **Missing `thread_id` in Checkpoints** | Trying to use `app.get_state()` or pause/resume without providing `{"configurable": {"thread_id": "xxx"}}`. | LangGraph persistence requires a `thread_id` to identify which distinct user session's state graph is being tracked. |

---

## 7. Hands-on Lab: Multi-Agent Research & Editor System

### Objective:
Build a two-agent system where a **Researcher** gathers bullet points on a topic, an **Editor** converts them into a polished markdown summary, and an **Auditor** inspects word count.

### Instructions:
1. Create state with `topic: str`, `research_notes: List[str]`, `final_article: str`, `word_count: int`.
2. Connect `START -> researcher -> editor -> auditor -> END`.
3. Add a check: if `word_count < 20`, route back to `editor` with instructions to expand.

```python
# lab_day31.py
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

class ArticleState(TypedDict):
    topic: str
    research_notes: List[str]
    final_article: str
    word_count: int

def researcher(state: ArticleState) -> dict:
    notes = [
        f"{state['topic']} is evolving rapidly in 2026.",
        "Agentic AI uses autonomous reasoning and tool execution.",
        "Stateful graphs provide predictable control loops."
    ]
    return {"research_notes": notes}

def editor(state: ArticleState) -> dict:
    summary = f"# Report on {state['topic']}\n\n" + " ".join(state["research_notes"])
    return {
        "final_article": summary,
        "word_count": len(summary.split())
    }

def auditor(state: ArticleState) -> dict:
    print(f"Auditor checked article: {state['word_count']} words.")
    return {}

graph = StateGraph(ArticleState)
graph.add_node("researcher", researcher)
graph.add_node("editor", editor)
graph.add_node("auditor", auditor)

graph.add_edge(START, "researcher")
graph.add_edge("researcher", "editor")
graph.add_edge("editor", "auditor")
graph.add_edge("auditor", END)

app = graph.compile()
result = app.invoke({"topic": "Agentic AI Frameworks"})
print(result["final_article"])
```

---

## 8. Top 3 Interview Questions & Answers

### Q1: Why use LangGraph instead of classic LangChain SequentialChains?
**Answer:**
Classic LangChain chains are Directed Acyclic Graphs (DAGs) without native support for loops, branching, or dynamic persistence. Production AI workflows require cycles (self-correction, code execution retry loops), state rollbacks, and long-running human approval pauses. LangGraph models computation as a state machine where nodes update a shared state dict, and edges can be conditional and cyclic, backed by built-in state checkpointing.

### Q2: How does Human-in-the-Loop (HITL) work in LangGraph under the hood?
**Answer:**
LangGraph utilizes checkpointing (e.g., `MemorySaver`, `SqliteSaver`, or `PostgresSaver`). By configuring `interrupt_before=["node_name"]` or `interrupt_after=["node_name"]`, the compiled graph yields control back to the caller right before/after that node executes, serializing the state to the checkpointer keyed by `thread_id`. The application can wait minutes, hours, or days for a human approval via web UI or API, and then resume execution by calling `app.stream(None, config={"configurable": {"thread_id": "..."}})`.

### Q3: What is the purpose of Reducers in LangGraph State?
**Answer:**
By default, when a node returns a dictionary key (e.g., `{"count": 5}`), LangGraph overwrites the existing value in state. Reducers (defined using `typing.Annotated[Type, reducer_function]`, such as `operator.add` or custom merge functions) specify *how* to combine existing state with new values. For instance, in chat conversations or event logs, we want to append new messages rather than replace past turns, which is solved cleanly by reducers.
