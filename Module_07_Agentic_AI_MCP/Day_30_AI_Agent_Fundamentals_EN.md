# Day 30: AI Agent Fundamentals (The ReAct Loop & Autonomous Systems)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The evolution: **Chatbots** vs **Chains** vs **Autonomous AI Agents**.
2. The core Agent cognitive architecture: **Planning**, **Tool Use**, **Observation**, and **Memory**.
3. The **ReAct (Reason + Act)** loop pattern.
4. Managing Agent State and defining strict task boundaries.
5. Single-Agent vs Multi-Agent architectures (Manager-Worker hierarchies).

---

## 1. The "Why": Chatbots Chat, Agents DO!

Let's understand the massive leap in software capabilities:
- **Chatbot (Passive)**: You ask *"Can you book a flight from Hyderabad to Bengaluru for tomorrow?"* $\rightarrow$ The chatbot replies: *"Sure, here are some airlines that fly between those cities! Good luck!"*
- **Fixed Workflow (Rigid)**: Hardcoded `if-else` script. If the airline website changes button layout, the script crashes.
- **AI Agent (Active & Autonomous)**:
  1. **Reasons**: *"I need to check flights for tomorrow."*
  2. **Acts**: Calls flight search API.
  3. **Observes**: *"Indigo is ₹4,200 at 10 AM, Air India is ₹6,000 at 2 PM."*
  4. **Reasons**: *"The user specified a budget under ₹5,000. Indigo is optimal."*
  5. **Acts**: Triggers payment gateway and emails the ticket PDF!

**An AI Agent is an LLM equipped with tools, working memory, and an autonomous loop to solve multi-step goals without continuous human babysitting.**

---

## 2. The Cognitive Anatomy of an Agent

```
┌──────────────────────────────────────────────────────────────┐
│                       THE AI AGENT BRAIN                     │
│                                                              │
│  ┌─────────────────┐   ┌─────────────────┐   ┌────────────┐  │
│  │    PLANNING     │   │     MEMORY      │   │   TOOLS    │  │
│  │ Decomposes goals│   │ Short-term (RAM)│   │ Python APIs│  │
│  │ into sub-tasks  │   │ Long-term (RAG) │   │ SQL, Web   │  │
│  └─────────────────┘   └─────────────────┘   └────────────┘  │
│                                                              │
│                      THE ReAct LOOP                          │
│                                                              │
│     Thought (Reasoning) ──► Action (Tool Call) ──►           │
│                                                              │
│     Observation (Result) ──► Thought (Next Step) ──► ...     │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. The ReAct (Reason + Act) Pattern

Introduced in a seminal 2022 research paper, **ReAct** prevents agents from hallucinating by forcing them to alternate between **verbal reasoning** and **concrete environment observation**:

```text
Question: Who was the Prime Minister of the UK when the first iPhone was released?

Thought 1: I need to find the exact release date of the first iPhone.
Action 1: search_wikipedia("first iPhone release date")
Observation 1: The original iPhone was released in the United States on June 29, 2007.

Thought 2: Now I need to find who was the Prime Minister of the UK on June 29, 2007.
Action 2: search_wikipedia("Prime Minister of United Kingdom 2007")
Observation 2: Tony Blair resigned on June 27, 2007, and Gordon Brown took office on June 27, 2007.

Thought 3: On June 29, 2007, Gordon Brown was in office. I have sufficient verified information.
Final Answer: Gordon Brown was the Prime Minister of the UK when the first iPhone was released.
```

---

## 4. Single-Agent vs Multi-Agent Systems

When tasks become complex, putting 20 tools into a single agent causes tool confusion and infinite loops.
**Multi-Agent Architecture** splits responsibilities:

```
                  ┌──────────────────────┐
                  │   SUPERVISOR AGENT   │
                  │  (Plans & Delegates) │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   ┌─────────────────┐               ┌─────────────────┐
   │ RESEARCH AGENT  │               │ WRITER AGENT    │
   │ Tools: Web, SQL │               │ Tools: Markdown │
   └─────────────────┘               └─────────────────┘
```

---

## 5. Common Fresher Pitfalls

1. **The Infinite Tool Loop (Cost Explosion)**:
   - If an API returns an unexpected error format, a poorly bounded agent will call that failing tool 500 times in a row until your API credits run out! **Always enforce `max_iterations = 5`**.
2. **Giving agents dangerous tools without guardrails**:
   - Never give an autonomous agent destructive tools (`drop_table`, `send_wire_transfer`, `delete_repo`) without an explicit **Human-in-the-Loop** checkpoint!
3. **Bloating Agent Memory**:
   - Accumulating raw tool outputs (e.g. 10 MB of raw HTML from a web scraper) directly into the agent's context window burns tokens rapidly. Summarize observations before appending to memory.

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: Build a Pure Python ReAct Autonomous Agent from Scratch
**Scenario**: Build an autonomous research agent that reasons through multi-step arithmetic and factual lookups, invoking external calculator and search tools until it converges on a final answer.

```python
# =========================================================
# Day 30 Lab: Autonomous ReAct Agent from Scratch
# =========================================================
import re
from google import genai
from google.genai import types

# 1. Custom Tools
def calculator(expression: str) -> str:
    """Evaluates basic mathematical expressions safely."""
    print(f"  🔧 [TOOL: Calculator] Evaluating: '{expression}'")
    try:
        # Safe evaluation of basic math
        allowed = set("0123456789+-*/.() ")
        if not set(expression).issubset(allowed):
            return "ERROR: Forbidden characters in expression."
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def lookup_tech_fact(entity: str) -> str:
    """Database lookup for technology release years and founding dates."""
    print(f"  🔧 [TOOL: FactLookup] Searching entity: '{entity}'")
    MOCK_DB = {
        "python": "Python was conceived in December 1989 by Guido van Rossum.",
        "transformers": "The Transformer architecture was introduced by Google in 2017.",
        "gemini": "Google announced the Gemini model family in December 2023."
    }
    return MOCK_DB.get(entity.lower().strip(), "Entity not found in local database.")

AVAILABLE_TOOLS = {
    "calculator": calculator,
    "lookup_tech_fact": lookup_tech_fact
}

# 2. ReAct System Prompt
REACT_PROMPT = """
You are an autonomous AI Agent solving questions step-by-step using tools.
You MUST follow this exact format:

Thought: Describe what you need to do next.
Action: tool_name(argument)
Observation: The tool output will appear here.
... (repeat Thought/Action/Observation N times)
Thought: I now know the final answer.
Final Answer: Your final answer to the user.

Available Tools:
- calculator(expression): Solves math equations like "2023 - 1989"
- lookup_tech_fact(entity): Looks up founding/release facts for entities like "python", "transformers", "gemini"
"""

def run_react_agent(user_query: str, max_steps: int = 5):
    print("="*60)
    print(f"AGENT GOAL: {user_query}")
    print("="*60)

    client = genai.Client()
    current_prompt = f"{REACT_PROMPT}\n\nQuestion: {user_query}\n"

    for step in range(1, max_steps + 1):
        print(f"\n--- STEP {step} ---")
        
        # 1. LLM Reasons and proposes Action
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=current_prompt,
            config=types.GenerateContentConfig(temperature=0.0, stop_sequences=["Observation:"])
        )
        
        step_text = response.text.strip()
        print(step_text)
        current_prompt += f"{step_text}\n"

        # Check if model arrived at Final Answer
        if "Final Answer:" in step_text:
            print("\n🎉 Goal Accomplished!")
            break

        # 2. Extract Action: tool_name(argument)
        match = re.search(r"Action:\s*(\w+)\((.*?)\)", step_text)
        if match:
            tool_name = match.group(1).strip()
            tool_arg = match.group(2).strip().strip("'\"")

            if tool_name in AVAILABLE_TOOLS:
                tool_result = AVAILABLE_TOOLS[tool_name](tool_arg)
            else:
                tool_result = f"Error: Tool '{tool_name}' does not exist."

            observation_str = f"Observation: {tool_result}"
            print(observation_str)
            current_prompt += f"{observation_str}\n"
        else:
            print("⚠️ No valid Action detected. Halting loop.")
            break

if __name__ == "__main__":
    run_react_agent("How many years passed between the conception of Python and the introduction of Transformers?")
```

---

## 7. Interview Quick-Fire Questions

1. **Q: What is the fundamental difference between a Chain and an Agent?**
   - **Answer**: A **Chain** executes a fixed, deterministic sequence of steps hardcoded by the developer (e.g. Prompt $\rightarrow$ Model $\rightarrow$ Parser). An **Agent** uses the LLM as a dynamic reasoning engine to actively decide which tools to invoke, in what order, and whether additional iterations are required based on real-time observations from the environment.
2. **Q: What is the ReAct loop and why is it superior to pure action-taking?**
   - **Answer**: ReAct combines **Reasoning** (Chain-of-Thought planning) and **Acting** (Tool execution) in a synergistic loop. Without reasoning, models take blind, uncoordinated actions. Without acting, models hallucinate facts from parametric memory. ReAct grounds each action in deliberate thought and evaluates the observation before taking the next step.
3. **Q: Why are multi-agent systems often preferred over a single complex agent?**
   - **Answer**: As an agent's tool count and task complexity increase, single-agent context windows become polluted with irrelevant instructions, causing tool hallucination, context drift, and loop failures. Multi-agent systems apply separation of concerns: specialized worker agents operate in narrow domains with clean context windows, coordinated by a supervisor agent.
