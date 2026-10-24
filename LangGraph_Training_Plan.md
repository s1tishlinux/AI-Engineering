# LangGraph Training Plan

## Overview

This document outlines a comprehensive training plan for learning LangGraph, covering five levels from beginner to production. The suggested durations assume participants already have basic Python knowledge.

## Prerequisites (Level 0: 2–3 days)

### Python
- Functions
- Classes
- Type hints
- TypedDict
- Async/await

### LLM Basics
- Prompts
- Tokens
- Temperature
- Chat message roles

### Tool / Function Calling
- How a model asks to call a function

### LangChain Basics
- Chat models
- Messages
- @tool
- Prompt templates (LangGraph builds on these)

## Core Building Blocks (Level 1: Week 1)

### Graph Basics
- StateGraph
- Nodes
- Edges
- START / END
- compile()
- invoke()

### State
- Defining state with TypedDict or Pydantic
- MessagesState

### Reducers
- How state updates merge (e.g., Annotated[list, add_messages])

### Conditional Edges
- add_conditional_edges for routing, branching, and loops

### Tools
- ToolNode
- tools_condition
- Binding tools to a model

### First Agent
- Build a ReAct agent by hand
- Compare with the prebuilt agent

### Project
- Q&A bot that calls 2–3 tools (e.g., search, calculator, policy lookup)

## Memory and Control (Level 2: Week 2)

### Checkpointers
- InMemorySaver
- SqliteSaver
- PostgresSaver
- thread_id

### Short-term Memory
- Conversation history per thread
- Trimming and summarizing messages

### Long-term Memory
- The Store API for memory across threads (user preferences, facts)

### Human-in-the-loop
- interrupt()
- Resuming with Command
- Approve/edit/reject patterns

### Time Travel
- get_state_history
- Replaying and forking from an earlier step

### Streaming
- Stream modes: values, updates, messages (tokens), custom

### Project
- Leave-request agent that pauses for manager approval before submitting

## Advanced Patterns (Level 3: Week 3)

### Subgraphs
- Nesting graphs and sharing state between parent and child

### Parallelism / Map-reduce
- The Send API for fan-out and fan-in

### Multi-agent Architectures
- Supervisor
- Hierarchical
- Swarm/handoffs (langgraph-supervisor, langgraph-swarm)

### Command Routing
- Updating state and choosing the next node in one step

### Agentic RAG
- Retrieve, grade documents
- Rewrite the query
- Generate an answer

### Functional API
- @entrypoint / @task as an alternative to explicit graphs

### MCP Integration
- Loading tools from MCP servers

### Project
- Multi-agent HR assistant where a supervisor routes to policy, payroll, and recruiting agents

## Production Readiness (Level 4: Week 4)

### Error Handling
- Retry policies
- recursion_limit
- Fallbacks
- Timeouts

### Observability
- LangSmith tracing and debugging failed runs

### Evaluation
- Datasets
- Trajectory evals
- LLM-as-judge
- Regression testing

### Testing
- Unit-testing nodes
- Mocking LLMs
- Testing routing logic

### Guardrails and Security
- Input/output validation
- Prompt-injection defense
- Tool permissions

### Cost and Latency
- Caching
- Choosing smaller models per node
- Token budgets

### Deployment
- LangGraph CLI
- LangGraph Studio
- Docker
- LangGraph Platform vs. self-hosting with FastAPI

### Capstone
- Deploy the Week 3 assistant with persistence, tracing, an eval suite, and a human-approval step

## Assessment Ideas

### Weekly
- Hands-on build reviewed against a rubric (works, handles errors, readable state design)

### Final
- Capstone demo plus a short design write-up on why they chose that graph structure

## Notes

LangGraph's APIs change fairly often. The 1.0 release moved some prebuilt agents into LangChain, so build the material against the current docs at [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph) and LangChain Academy's free Introduction to LangGraph course.

## Trainer Notes

- Prepare hands-on exercises for each level
- Provide cheat sheets for quick reference
- Encourage Q&A sessions during breaks
- Offer office hours for additional support

## Evaluation Scorecards

### Weekly Evaluation

| Criteria | Excellent (5) | Good (3) | Needs Improvement (1) |
|----------|----------------|---------------|-----------------------|
| Completion | 100% | 75-99% | <75% |
| Error Handling | Excellent | Good | Poor |
| State Design | Excellent | Good | Poor |

### Final Evaluation

| Criteria | Excellent (5) | Good (3) | Needs Improvement (1) |
|----------|----------------|---------------|-----------------------|
| Capstone Demo | Excellent | Good | Poor |
| Design Write-up | Excellent | Good | Poor |
| Overall Understanding | Excellent | Good | Poor |

This training plan provides a structured approach to learning LangGraph, from foundational concepts to advanced patterns and production readiness. It includes hands-on projects, assessments, and resources for continuous learning.