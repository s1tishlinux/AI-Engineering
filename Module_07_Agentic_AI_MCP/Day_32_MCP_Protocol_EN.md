# Day 32: Model Context Protocol (MCP) & Tool Interoperability 🔌

---

## 1. Day 32 Learning Objectives
- Understand why the **Model Context Protocol (MCP)** is revolutionizing how AI models connect to data, databases, and enterprise tools.
- Learn the core MCP architecture: **Host (e.g. IDE / Client App)**, **Client**, and **Server**.
- Master the three primary MCP primitives: **Resources** (file-like read data), **Tools** (executable functions with side effects), and **Prompts** (pre-composed contextual workflows).
- Build a custom **MCP Server in Python** using FastMCP / standard MCP SDK over both `stdio` and `SSE` (Server-Sent Events) transports.
- Address agent security, sandbox permissions, and safe execution boundaries when exposing real infrastructure to LLMs.

---

## 2. Real-World Analogy

> 💡 **Analogy: Proprietary Phone Chargers vs. Universal USB-C**
>
> - **Before MCP (The Fragile Adapter Mess):**
>   Imagine every mobile phone company, camera maker, and laptop manufacturer invented their own custom, proprietary charging cables and ports. If you bought a new phone, all your old cables were useless.
>   In AI, every tool was a custom custom-coded wrapper: LangChain tool schemas, OpenAI function definitions, LlamaIndex readers, Claude tool specs. If you wrote a PostgreSQL connector for OpenAI, you had to re-write it completely to use it inside Claude Desktop or another agent platform.
> - **With MCP (The Universal USB-C Standard):**
>   MCP is the **USB-C port for AI**!
>   You write your PostgreSQL or Git server once as an **MCP Server**. Any **MCP Host** (Cursor, Claude Desktop, Antigravity IDE, your custom LangGraph agent) plugs into it instantly via a single standard JSON-RPC protocol. No custom glue code needed!

---

## 3. Architecture Overview: How MCP Works

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MCP HOST (e.g., Claude Desktop, IDE, Agent App) │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │        LLM Engine         │      │         MCP Client          │   │
│   │  (Generates Function Call)│◄────►│  (Translates to JSON-RPC)   │   │
│   └───────────────────────────┘      └──────────────┬──────────────┘   │
└─────────────────────────────────────────────────────┼──────────────────┘
                                                      │
                       Protocol Transport (JSON-RPC over stdio or SSE)
                                                      │
                                                      ▼
┌────────────────────────────────────────────────────────────────────────┐
│                              MCP SERVER                                │
│                                                                        │
│   ┌────────────────────────┐  ┌─────────────────┐  ┌───────────────┐   │
│   │       RESOURCES        │  │      TOOLS      │  │    PROMPTS    │   │
│   │ (Read data: logs, DB)  │  │ (Actions, APIs) │  │ (Templates)   │   │
│   └────────────────────────┘  └─────────────────┘  └───────────────┘   │
│                                                                        │
│   Underlying Services:                                                 │
│   - Local Filesystem       - PostgreSQL / MySQL    - GitHub APIs       │
└────────────────────────────────────────────────────────────────────────┘
```

### The Three MCP Primitives:
1. **Resources:** Read-only data sources that clients can inspect (e.g., `file:///var/log/app.log`, `postgres://schema/users`). Similar to GET endpoints.
2. **Tools:** Callable functions with side-effects that LLMs can invoke (e.g., `create_git_branch(name)`, `send_slack_message(channel, text)`).
3. **Prompts:** Reusable templates and conversational recipes exposed by the server to guide user interactions (e.g., `analyze_code_review(pr_id)`).

---

## 4. MCP Communication Transports

1. **`stdio` (Standard Input / Output):**
   - The Host launches the MCP server as a local child process.
   - Messages are sent back and forth line-by-line as JSON-RPC over stdin/stdout.
   - Ideal for local tools, filesystems, and developer environments.
2. **`SSE` (Server-Sent Events over HTTP):**
   - The MCP server runs as a separate web service over network ports.
   - Server streams responses via SSE; client posts commands via HTTP POST.
   - Ideal for remote cloud services, shared enterprise tools, and microservices.

---

## 5. Coding Walkthrough: Building an MCP Server in Python

Here is a complete, clean Python implementation of an MCP server providing database analysis tools using the official standard specification:

```python
# mcp_data_server.py
"""
Sample MCP Server built with Python FastMCP
Requirements:
  pip install mcp
"""
import json
import sqlite3
from typing import Dict, Any, List

# For demonstration, we simulate FastMCP server primitives
class SimpleMCPServer:
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.resources = {}
        
    def tool(self, name: str, description: str):
        """Decorator to register an executable tool."""
        def decorator(func):
            self.tools[name] = {
                "name": name,
                "description": description,
                "func": func
            }
            return func
        return decorator

    def resource(self, uri: str, description: str):
        """Decorator to register a read-only resource."""
        def decorator(func):
            self.resources[uri] = {
                "uri": uri,
                "description": description,
                "func": func
            }
            return func
        return decorator

    def handle_json_rpc(self, request_str: str) -> str:
        """Processes incoming JSON-RPC protocol messages."""
        req = json.loads(request_str)
        method = req.get("method")
        msg_id = req.get("id")
        
        # 1. Handshake / List Tools
        if method == "tools/list":
            tool_list = [
                {"name": v["name"], "description": v["description"]}
                for v in self.tools.values()
            ]
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tool_list}})
            
        # 2. Call Tool
        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})
            
            if name in self.tools:
                try:
                    result = self.tools[name]["func"](**args)
                    return json.dumps({
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {"content": [{"type": "text", "text": str(result)}]}
                    })
                except Exception as e:
                    return json.dumps({
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"code": -32000, "message": str(e)}
                    })
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Tool not found"}})
            
        # 3. Read Resource
        elif method == "resources/read":
            params = req.get("params", {})
            uri = params.get("uri")
            if uri in self.resources:
                data = self.resources[uri]["func"]()
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"contents": [{"uri": uri, "text": data}]}
                })
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Resource not found"}})
            
        return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not supported"}})

# Instantiate Server
server = SimpleMCPServer(name="AnalyticsServer")

# Register Read-only Resource
@server.resource(uri="system://health", description="Returns current database and host health stats")
def get_system_health() -> str:
    return json.dumps({"status": "HEALTHY", "active_connections": 14, "disk_usage_pct": 42.1})

# Register Executable Tools
@server.tool(name="execute_sql_query", description="Executes a safe read-only SQL query on analytics DB")
def execute_sql_query(query: str) -> str:
    # Security guardrail: Reject destructive commands
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
    if any(keyword in query.upper() for keyword in forbidden):
        raise ValueError("Security violation: Only SELECT queries are permitted.")
        
    # Mocking SQLite in-memory execution
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE sales (region TEXT, revenue INT)")
    cursor.execute("INSERT INTO sales VALUES ('South', 50000), ('North', 75000), ('East', 32000)")
    
    cursor.execute(query)
    rows = cursor.fetchall()
    return json.dumps({"columns": [desc[0] for desc in cursor.description], "rows": rows})

# Demo JSON-RPC Client Execution
if __name__ == "__main__":
    print("--- 1. Client Requests Available Tools ---")
    req_list = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    print("Request :", req_list)
    print("Response:", server.handle_json_rpc(req_list))
    
    print("\n--- 2. Client Calls 'execute_sql_query' Tool ---")
    req_call = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "execute_sql_query",
            "arguments": {"query": "SELECT region, revenue FROM sales WHERE revenue > 40000"}
        }
    })
    print("Request :", req_call)
    print("Response:", server.handle_json_rpc(req_call))
    
    print("\n--- 3. Client Attempts Blocked Mutation (Security Guardrail) ---")
    req_blocked = json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "execute_sql_query",
            "arguments": {"query": "DROP TABLE sales"}
        }
    })
    print("Request :", req_blocked)
    print("Response:", server.handle_json_rpc(req_blocked))
```

---

## 6. Common Fresher Pitfalls

| Pitfall | Root Cause | Best Practice |
| :--- | :--- | :--- |
| **Writing `print()` statements in `stdio` servers** | In `stdio` transport, stdout is the raw communication wire for JSON-RPC messages. Calling normal `print("debug log")` corrupts the JSON stream and crashes the client! | Never write raw `print()` to stdout. Log strictly to `stderr` (`sys.stderr.write(...)`) or use standard logging configured to files. |
| **Exposing Unrestricted Shell / DB execution** | Giving an MCP tool raw bash execution without whitelisting allows prompt injection attacks to compromise host systems. | Always enforce principle of least privilege: read-only database connections, explicit parameter schemas, and sanitization. |
| **Ignoring Network Timeouts on SSE** | When hosting remote MCP servers over HTTP/SSE, long-running agent tasks can trigger proxy timeouts (HTTP 504). | Implement background task IDs with status polling or stream partial heartbeats over SSE. |

---

## 7. Hands-on Lab: Custom Filesystem Explorer MCP Server

### Objective:
Build an MCP server that safely exposes a designated directory:
1. Resource: `files://list` returning a list of `.txt` and `.md` files.
2. Tool: `read_file(filename)` returning the file's content (blocking paths outside the folder like `../etc/passwd`).

```python
# lab_day32_mcp.py
import os

SAFE_DIR = os.path.abspath("./sandbox")
os.makedirs(SAFE_DIR, exist_ok=True)
with open(os.path.join(SAFE_DIR, "notes.txt"), "w") as f:
    f.write("MCP allows universal AI tool integration.")

def safe_read_file(filename: str) -> str:
    target_path = os.path.abspath(os.path.join(SAFE_DIR, filename))
    # Directory traversal defense
    if not target_path.startswith(SAFE_DIR):
        raise PermissionError("Access denied: Path traversal detected!")
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"File {filename} does not exist.")
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()

print("Safe read test:", safe_read_file("notes.txt"))
```

---

## 8. Top 3 Interview Questions & Answers

### Q1: What is the difference between an MCP Client and an MCP Server?
**Answer:**
- An **MCP Client** resides inside the AI application or Host (such as Claude Desktop, an IDE, or an agent runtime). It handles the connection to one or more MCP servers, translates LLM tool-calling intentions into standard JSON-RPC requests, and passes observations back to the LLM.
- An **MCP Server** is a lightweight program that exposes specific data (Resources), actions (Tools), or prompt templates to any connected client via the standard protocol without knowing which LLM is querying it.

### Q2: How does MCP differ from REST APIs?
**Answer:**
REST APIs are designed for human software developers and microservice web endpoints, lacking standard metadata for LLM context, schema discovery, sampling, and prompt templates. MCP is explicitly built for AI interaction: it standardizes resource discovery, tool description schemas (JSON Schema), dynamic context subscriptions, and bidirectional execution handshakes via JSON-RPC.

### Q3: Why is standardizing on `stdio` vs `SSE` important in MCP?
**Answer:**
- `stdio` allows zero-network, ultra-secure local execution: the host manages the server's lifecycle as a child process with no open network ports or credentials exposed over the web.
- `SSE` (Server-Sent Events) is crucial when tools run as enterprise services in Kubernetes, private clouds, or multi-tenant architectures where clients and servers live on different machines.
