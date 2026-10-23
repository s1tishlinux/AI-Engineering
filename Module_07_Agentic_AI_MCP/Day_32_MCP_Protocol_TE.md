# Day 32: Model Context Protocol (MCP) & టూల్ ఇంటరాపరేబిలిటీ 🔌

---

## 1. ఈ రోజు మన గోల్స్ (Day 32 Learning Objectives)
- **Model Context Protocol (MCP)** అంటే ఏమిటి? ఆర్టిఫిషియల్ ఇంటెలిజెన్స్ రంగంలో ఇది విప్లవాత్మక ప్రమాణంగా (Open Standard) ఎందుకు మారింది?
- MCP ఆర్కిటెక్చర్ లోని 3 ప్రధాన విభాగాలు: **Host (యాప్/IDE)**, **Client (కనెక్టర్)**, మరియు **Server (డేటా/టూల్ ప్రొవైడర్)**.
- MCP లోని 3 కోర్ ప్రిమిటివ్స్: **Resources** (రీడ్-ఓన్లీ డేటా), **Tools** (ఎగ్జిక్యూటబుల్ ఫంక్షన్స్), మరియు **Prompts** (రీయూజబుల్ వర్క్‌ఫ్లోలు).
- Python ఉపయోగించి సొంత **MCP Server** ని తయారుచేయడం మరియు `stdio`, `SSE` ట్రాన్స్‌పోర్ట్స్ అర్థం చేసుకోవడం.
- ఏజెంట్లకు బాహ్య సిస్టమ్స్ (డేటాబేస్, ఫైల్ సిస్టమ్) యాక్సెస్ ఇచ్చేటప్పుడు పాటించాల్సిన సెక్యూరిటీ మరియు గార్డ్‌రెయిల్స్.

---

## 2. రియల్ వరల్డ్ అనలాజీ (Real-World Analogy)

> 💡 **అనలాజీ: పాతకాలం నాటి విభిన్న ఛార్జర్లు vs యూనివర్సల్ USB-C పోర్ట్**
>
> - **MCP కి ముందు (గందరగోళం):**
>   ఒకప్పుడు నోకియాకి సన్నపిన్ ఛార్జర్, సోనీకి వేరే పిన్, శామ్‌సంగ్ కి ఇంకో పిన్ ఉండేవి. ఒక ఫోన్ ఛార్జర్ ఇంకో ఫోన్ కి పనికివచ్చేది కాదు.
>   AI లో కూడా అంతే: మీరు ఒక PostgreSQL టూల్ రాస్తే, అది OpenAI కి ఒకలా రాయాలి, LangChain కి ఇంకోలా రాయాలి, Claude కి వేరే ఫార్మాట్ లో రాయాలి. ఒక్కో ప్లాట్‌ఫారమ్ కి మళ్ళీ మళ్ళీ కోడ్ మార్చాల్సి వచ్చేది.
> - **MCP వచ్చిన తర్వాత (యూనివర్సల్ విప్లవం):**
>   MCP అనేది **AI కోసం వచ్చిన USB-C పోర్ట్ లాంటిది**!
>   మీరు ఒకసారి మీ డేటాబేస్ లేదా గిట్‌హబ్ కోసం **MCP Server** రాస్తే చాలు. Cursor IDE, Claude Desktop, Antigravity IDE, లేదా మీ పైథాన్ ఏజెంట్ ఏదైనా సరే.. ఒకే ఒక్క సింగిల్ కేబుల్ (JSON-RPC Protocol) తో ప్లగ్ చేసి క్షణాల్లో వాడుకోవచ్చు!

---

## 3. MCP ఆర్కిటెక్చర్ ఎలా పనిచేస్తుంది?

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MCP HOST (ఉదా: Claude Desktop, IDE, Agent App)  │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │        LLM Engine         │      │         MCP Client          │   │
│   │   (ఏ టూల్ కావాలో చెప్తుంది)│◄────►│ (JSON-RPC మెసేజ్ గా మారుస్తుంది)│ │
│   └───────────────────────────┘      └──────────────┬──────────────┘   │
└─────────────────────────────────────────────────────┼──────────────────┘
                                                      │
                       ప్రోటోకాల్ ట్రాన్స్‌పోర్ట్ (JSON-RPC over stdio / SSE)
                                                      │
                                                      ▼
┌────────────────────────────────────────────────────────────────────────┐
│                              MCP SERVER                                │
│                                                                        │
│   ┌────────────────────────┐  ┌─────────────────┐  ┌───────────────┐   │
│   │       RESOURCES        │  │      TOOLS      │  │    PROMPTS    │   │
│   │ (డేటా చదవడం: Logs, DB) │  │(పనులు: APIs, SQL)│  │ (టెంప్లేట్లు) │   │
│   └────────────────────────┘  └─────────────────┘  └───────────────┘   │
│                                                                        │
│   కనెక్ట్ అయ్యే సిస్టమ్స్:                                             │
│   - కంప్యూటర్ ఫైల్ సిస్టమ్   - PostgreSQL డేటాబేస్ - GitHub / Slack APIs │
└────────────────────────────────────────────────────────────────────────┘
```

### MCP లోని 3 ముఖ్యమైన కాన్సెప్ట్స్:
1. **Resources (రిసోర్సెస్):** రీడ్-ఓన్లీ డేటా. అంటే కేవలం సమాచారాన్ని చదవడానికి మాత్రమే (ఉదా: `logs://today.log`, `postgres://schema/orders`). ఇవి డేటాని మార్చలేవు.
2. **Tools (టూల్స్):** సిస్టమ్ లో మార్పులు చేయగల ఎగ్జిక్యూటబుల్ ఫంక్షన్స్ (ఉదా: `send_slack_message(channel, text)`, `run_sql_query(query)`).
3. **Prompts (ప్రాంప్ట్స్):** ముందే తయారుచేసిన ప్రాంప్ట్ టెంప్లేట్లు. యూజర్ కి పనులను సులభతరం చేయడానికి సర్వర్ అందించే గైడెన్స్.

---

## 4. ట్రాన్స్‌పోర్ట్ రకాలు (Transports)

1. **`stdio` (Standard Input / Output):**
   - మీ లోకల్ కంప్యూటర్ లో హోస్ట్ యాప్ ఒక చైల్డ్ ప్రాసెస్ గా సర్వర్ ని రన్ చేస్తుంది.
   - నెట్‌వర్క్ పోర్ట్స్ అవసరం లేదు, పూర్తి సురక్షితం. కన్సోల్ పైప్స్ ద్వారా JSON-RPC మెసేజ్‌లు వెళ్తాయి.
2. **`SSE` (Server-Sent Events over HTTP):**
   - సర్వర్ క్లౌడ్ లో లేదా వేరే రిమోట్ మెషిన్ లో నడుస్తున్నప్పుడు HTTP పోర్ట్ ద్వారా కనెక్ట్ అవుతుంది.
   - రిమోట్ మైక్రోసర్వీసెస్ కి మరియు మల్టీ-యూజర్ టీమ్స్ కి ఇది ఉపయోగపడుతుంది.

---

## 5. కోడింగ్ వాక్‌త్రూ: Python లో ఒక MCP Server తయారుచేయడం

కింది కోడ్ స్వచ్ఛమైన పైథాన్ లో JSON-RPC స్టాండర్డ్ తో పనిచేసే ఒక చిన్న డేటాబేస్ MCP సర్వర్ ని చూపిస్తుంది:

```python
# simple_mcp_server.py
import json
import sqlite3

class LocalMCPServer:
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.resources = {}
        
    def register_tool(self, name: str, description: str, func):
        self.tools[name] = {"description": description, "func": func}

    def register_resource(self, uri: str, description: str, func):
        self.resources[uri] = {"description": description, "func": func}

    def process_request(self, json_msg: str) -> str:
        data = json.loads(json_msg)
        method = data.get("method")
        msg_id = data.get("id")

        # 1. అందుబాటులో ఉన్న టూల్స్ లిస్ట్ అడిగినప్పుడు
        if method == "tools/list":
            tools_info = [{"name": k, "description": v["description"]} for k, v in self.tools.items()]
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools_info}})

        # 2. టూల్ ని ఎగ్జిక్యూట్ చేయమని అడిగినప్పుడు
        elif method == "tools/call":
            params = data.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            if name in self.tools:
                try:
                    result = self.tools[name]["func"](**arguments)
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
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "టూల్ దొరకలేదు"}})

        # 3. రిసోర్స్ చదవమని అడిగినప్పుడు
        elif method == "resources/read":
            uri = data.get("params", {}).get("uri")
            if uri in self.resources:
                content = self.resources[uri]["func"]()
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": content}})
                
        return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "చెల్లని మెథడ్"}})

# సర్వర్ ని సెటప్ చేద్దాం
server = LocalMCPServer(name="TelanganaAnalyticsServer")

# Resource రిజిస్ట్రేషన్
def get_status():
    return json.dumps({"system": "ONLINE", "database": "Postgres-Replica", "active_users": 128})

server.register_resource("system://status", "సిస్టమ్ హెల్త్ రిసోర్స్", get_status)

# Tool రిజిస్ట్రేషన్ (SQL Query Execution with Guardrails)
def query_sales_database(query: str):
    # సెక్యూరిటీ చెక్: కేవలం SELECT కి మాత్రమే అనుమతి
    forbidden = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "INSERT"]
    if any(word in query.upper() for word in forbidden):
        raise PermissionError("భద్రతా హెచ్చరిక: కేవలం డేటా చదవడానికి (SELECT) మాత్రమే అనుమతి ఉంది!")
        
    # డెమో కోసం ఇన్-మెమొరీ డేటాబేస్
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE products (name TEXT, price INT)")
    cur.execute("INSERT INTO products VALUES ('Laptop', 65000), ('Mouse', 1200), ('Monitor', 18000)")
    
    cur.execute(query)
    rows = cur.fetchall()
    return rows

server.register_tool(
    name="query_sales_database",
    description="వస్తువుల ధరల డేటాబేస్ పై సురక్షితమైన రీడ్-ఓన్లీ క్వెరీ రన్ చేస్తుంది.",
    func=query_sales_database
)

# రన్ చేసి టెస్ట్ చేద్దాం
if __name__ == "__main__":
    print("--- 1. క్లయింట్ టూల్స్ లిస్ట్ అడుగుతుంది ---")
    req1 = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    print("రెస్పాన్స్:", server.process_request(req1))

    print("\n--- 2. క్లయింట్ 'query_sales_database' టూల్ ని కాల్ చేస్తుంది ---")
    req2 = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "query_sales_database",
            "arguments": {"query": "SELECT * FROM products WHERE price > 5000"}
        }
    })
    print("రెస్పాన్స్:", server.process_request(req2))

    print("\n--- 3. ఒకవేళ ఏజెంట్ డేటాబేస్ ని డిలీట్ చేయాలని చూస్తే (గార్డ్‌రెయిల్ నిరోధిస్తుంది) ---")
    req3 = json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "query_sales_database",
            "arguments": {"query": "DROP TABLE products"}
        }
    })
    print("రెస్పాన్స్:", server.process_request(req3))
```

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు & జాగ్రత్తలు

| సాధారణ తప్పు | ఎందుకు ప్రమాదకరం? | సరైన మార్గం |
| :--- | :--- | :--- |
| **`stdio` సర్వర్ లో `print()` స్టేట్‌మెంట్స్ వాడటం** | `stdio` కమ్యూనికేషన్ లో stdout మొత్తం JSON-RPC మెసేజ్ ల కోసమే వాడబడుతుంది. అక్కడ మీ సొంత ప్రింట్స్ వేస్తే JSON కరప్ట్ అయ్యి క్లయింట్ క్రాష్ అవుతుంది! | డీబగ్ లాగ్స్ కోసం ఎప్పుడూ `sys.stderr.write()` లేదా ఫైల్ లాగింగ్ మాత్రమే వాడాలి. |
| **ఎటువంటి రెస్ట్రిక్షన్స్ లేకుండా OS Shell యాక్సెస్ ఇవ్వడం** | ఏజెంట్ కి కంప్యూటర్ టెర్మినల్ ని ఎలాంటి కంట్రోల్ లేకుండా ఇస్తే, ప్రాంప్ట్ ఇంజెక్షన్ వల్ల హ్యాకర్లు మీ ఫైల్స్ ని డిలీట్ చేయించగలరు. | టూల్స్ కి ఇచ్చే అనుమతులు చాలా స్పష్టంగా, కనీస స్థాయి (Principle of Least Privilege) లో మాత్రమే ఉండాలి. |
| **టూల్ పారామీటర్స్ కి టైప్స్ మరియు డిస్క్రిప్షన్స్ ఇవ్వకపోవడం** | డిస్క్రిప్షన్ సరిగ్గా లేకపోతే LLM ఆ టూల్ ని ఎప్పుడు వాడాలో అర్థం చేసుకోలేక తప్పుడు పారామీటర్స్ పంపుతుంది. | ప్రతి టూల్ కి చాలా స్పష్టమైన వివరణ మరియు Pydantic స్కీమా ఇవ్వాలి. |

---

## 7. ప్రాక్టికల్ ల్యాబ్ (Hands-on Lab)

### లక్ష్యం:
కంపెనీ లీవ్ మేనేజ్‌మెంట్ సిస్టమ్ కోసం ఒక చిన్న **Leave Management MCP Server** తయారుచేయండి:
1. `Resource`: `employee://leaves_balance` (ఉద్యోగికి మిగిలి ఉన్న సాధారణ మరియు అనారోగ్య సెలవుల సంఖ్యను చూపించాలి).
2. `Tool`: `apply_leave(employee_id, days, reason)` (సెలవు దరఖాస్తు చేసుకోవడానికి). మిగిలిన సెలవుల కంటే ఎక్కువ రోజుల కోసం దరఖాస్తు చేస్తే ఎర్రర్ రిటర్న్ చేయాలి.

---

## 8. టాప్ 3 ఇంటర్వ్యూ ప్రశ్నలు & సమాధానాలు

### Q1: Model Context Protocol (MCP) ఎందుకు అంత ప్రాచుర్యం పొందింది?
**సమాధానం:**
గతంలో ప్రతి AI కంపెనీ (OpenAI, Anthropic, LangChain) టూల్స్ కనెక్ట్ చేయడానికి వేర్వేరు ఫార్మాట్లను వాడేవి. దీనివల్ల డెవలపర్లు ఒకే టూల్ ని పలుమార్లు తిరగరాయాల్సి వచ్చేది. MCP ఒక యూనివర్సల్ ఓపెన్ స్టాండర్డ్ ని పరిచయం చేసింది. ఒక్కసారి MCP సర్వర్ డెవలప్ చేస్తే చాలు, దాన్ని ఏ AI మోడల్ లేదా IDE అయినా సులభంగా అనుసంధానం చేసుకోగలదు.

### Q2: MCP లో Resources కి మరియు Tools కి మధ్య తేడా ఏమిటి?
**సమాధానం:**
- **Resources:** ఇవి రీడ్-ఓన్లీ (Read-only) డేటా వనరులు. సిస్టమ్ లో ఎటువంటి మార్పులు చేయవు. కేవలం కాంటెక్స్ట్ కోసం చదవడానికి మాత్రమే ఉపయోగపడతాయి (ఉదా: లాగ్ ఫైల్స్, డేటాబేస్ స్కీమా).
- **Tools:** ఇవి ఎగ్జిక్యూటబుల్ పనులు (Actions). బాహ్య సిస్టమ్స్ లో మార్పులు తీసుకురాగలవు (ఉదా: ఈమెయిల్ పంపడం, ఫైల్ క్రియేట్ చేయడం, డేటాబేస్ లో రికార్డ్ యాడ్ చేయడం).

### Q3: MCP లో stdio ట్రాన్స్‌పోర్ట్ కి ఎందుకు ప్రాధాన్యత ఇస్తారు?
**సమాధానం:**
`stdio` (Standard I/O) లో సర్వర్ మీ లోకల్ కంప్యూటర్‌లోనే ఒక చైల్డ్ ప్రాసెస్‌గా నడుస్తుంది. దీనికి ఎటువంటి నెట్‌వర్క్ పోర్ట్‌లు ఓపెన్ చేయాల్సిన అవసరం లేదు, ఇంటర్నెట్ లో ఎక్స్‌పోజ్ అయ్యే రిస్క్ ఉండదు, మరియు కమ్యూనికేషన్ చాలా వేగంగా ఉంటుంది. డెవలపర్ టూల్స్ మరియు లోకల్ ఫైల్ సిస్టమ్స్ కి ఇది అత్యంత సురక్షితమైన మార్గం.
