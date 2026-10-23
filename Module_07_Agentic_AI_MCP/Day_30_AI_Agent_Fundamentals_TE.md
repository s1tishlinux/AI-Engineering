# Day 30: AI Agent Fundamentals & ReAct Pattern (AI ఏజెంట్ బేసిక్స్ & ReAct ప్యాటర్న్) 🤖

---

## 1. ఈ రోజు మన గోల్స్ (Day 30 Learning Objectives)
- సాధారణ Chatbot లేదా LLM కి, స్వయంప్రతిపత్తి కలిగిన **AI Agent** కి మధ్య గల అసలైన తేడాను అర్థం చేసుకోవడం.
- Agent ఆర్కిటెక్చర్ లోని 4 పిల్లర్స్: **Brain (LLM), Planning, Memory, Tools**.
- **ReAct Pattern (Reasoning + Acting)** వర్కింగ్ ప్రిన్సిపల్: `Thought -> Action -> Observation -> Final Answer`.
- Python లో స్వచ్ఛమైన `while` లూప్ మరియు Function Calling ఉపయోగించి స్క్రాచ్ నుండి Agent ని రూపొందించడం.
- Agent Infinite Loops, Tool Call Failures మరియు Parse Errors ని ఎలా హ్యాండిల్ చేయాలో నేర్చుకోవడం.

---

## 2. రియల్ వరల్డ్ అనలాజీ (Real-World Analogy)

> 💡 **అనలాజీ: కౌంటర్ క్లర్క్ vs పర్సనల్ ఎగ్జిక్యూటివ్ అసిస్టెంట్**
>
> - **సాధారణ LLM (Chatbot):** రైల్వే స్టేషన్ సమాచార కౌంటర్ లో కూర్చున్న వ్యక్తి లాంటిది. మీరు "హైదరాబాద్ నుండి ఢిల్లీ వెళ్ళే ట్రైన్ ఏది?" అని అడిగితే టైమ్ టేబుల్ చూసి చెప్తాడు. కానీ మీ బదులు టికెట్ బుక్ చేయలేడు, బ్యాంక్ అకౌంట్ నుండి పేమెంట్ చేయలేడు, లేదా మీ క్యాలెండర్ లో రిమైండర్ పెట్టలేడు.
> - **AI Agent:** మీ పర్సనల్ ఎగ్జిక్యూటివ్ అసిస్టెంట్ లాంటివాడు!
>   మీరు: *"రేపు పొద్దున్న 8 గంటలకు నేను ఢిల్లీ లో ఒక మీటింగ్ కి హాజరుకావాలి, ఏర్పాట్లు చేయి."* అని అడిగారనుకోండి.
>   Agent ఏం ఆలోచిస్తుంది (Reasoning):
>   1. *"మొదట హైదరాబాద్-ఢిల్లీ ఫ్లైట్ టైమింగ్స్ చూడాలి (Tool 1: Flight Search API)"*
>   2. *"సాయంత్రం 8 కి టికెట్ బుక్ చేయాలి (Tool 2: Payment API)"*
>   3. *"ఎయిర్‌పోర్ట్ దగ్గర హోటల్ రూమ్ బుక్ చేయాలి (Tool 3: Hotel API)"*
>   4. *"క్యాలెండర్ లో టికెట్ డీటైల్స్ యాడ్ చేయాలి (Tool 4: Google Calendar API)"*
>   ఒక్కో పని చేసి రిజల్ట్ చెక్ చేసుకుంటూ చివరకు: *"సార్, మీ ఫ్లైట్ మరియు హోటల్ బుకింగ్ పూర్తయ్యాయి, మీ క్యాలెండర్ లో ఈవెంట్ పెట్టాను!"* అని చెప్తాడు.

---

## 3. Agent కోర్ భాగాలు (Core Components of an AI Agent)

```
                     ┌──────────────────────────────┐
                     │          USER INPUT          │
                     └──────────────┬───────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                              AI AGENT                                  │
│                                                                        │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                          BRAIN (LLM)                           │   │
│   │              (Reasoning, Decision Making, Persona)             │   │
│   └───────────────▲───────────────────────────────┬────────────────┘   │
│                   │                               │                    │
│   ┌───────────────┴───────────────┐ ┌─────────────▼────────────────┐   │
│   │            MEMORY             │ │           PLANNING           │   │
│   │ - Short-term (Chat History)   │ │ - Sub-goal decomposition     │   │
│   │ - Long-term (Vector DB/Facts) │ │ - Reflection / Self-Critique │   │
│   └───────────────────────────────┘ └─────────────┬────────────────┘   │
│                                                   │                    │
│                                                   ▼                    │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                         ACTION / TOOLS                         │   │
│   │  [Search API]   [Calculator]   [Database Query]   [Send Email] │   │
│   └───────────────────────────────┬────────────────────────────────┘   │
└───────────────────────────────────┼────────────────────────────────────┘
                                    │
                                    ▼
                          ENVIRONMENT / REAL WORLD
```

1. **The Brain (LLM):** లాజిక్, లాంగ్వేజ్ ప్రాసెసింగ్ మరియు డెసిషన్ మేకింగ్.
2. **Planning (ప్లానింగ్):** సంక్లిష్టమైన సమస్యను చిన్న చిన్న పనులుగా (Sub-tasks) విభజించడం, పొరపాటు జరిగితే సరిదిద్దుకోవడం (Reflection).
3. **Memory (మెమొరీ):**
   - *Short-term Memory:* ప్రస్తుత సంభాషణ లోని మెసేజ్ హిస్టరీ.
   - *Long-term Memory:* గతంలో నేర్చుకున్న విషయాలు (Vector DB ఆధారంగా).
4. **Tools (టూల్స్):** బాహ్య ప్రపంచంతో సంభాషించడానికి API లు, కాలిక్యులేటర్లు, పైథాన్ ఇంటర్‌ప్రీటర్లు లేదా డేటాబేస్ లు.

---

## 4. ReAct ఆర్కిటెక్చర్ (Reasoning + Acting)

ReAct పేపర్ (Yao et al., 2022) ప్రకారం AI Agent కింది లూప్ లో పనిచేస్తుంది:

1. **Question:** యూజర్ ఇచ్చిన సమస్య.
2. **Thought:** సమస్యను సాధించడానికి నేను ఇప్పుడు ఏ సమాచారం తెలుసుకోవాలి? (లాజికల్ ఆలోచన)
3. **Action:** ఆలోచనను బట్టి ఏ టూల్ రన్ చేయాలి? ఉదా: `Search["హైదరాబాద్ వాతావరణం"]`
4. **Observation:** టూల్ తిరిగి ఇచ్చిన రిజల్ట్ (ఉదా: 32°C, Sunny).
5. **Thought:** నా దగ్గర యూజర్ కి సమాధానం చెప్పడానికి సరిపడా సమాచారం ఉందా?
6. అవును అంటే -> **Final Answer** ఇస్తుంది. లేకపోతే మళ్ళీ కొత్త Action తీసుకుంటుంది.

---

## 5. కోడింగ్ వాక్‌త్రూ: స్వచ్ఛమైన Python తో ReAct Agent

కింది కోడ్ ఎలాంటి భారీ లైబ్రరీలు (LangChain/LangGraph) లేకుండా స్వచ్ఛమైన Python లో ఒక ReAct Agent ఎలా రన్ అవుతుందో వివరిస్తుంది:

```python
import json
import re

# 1. మాక్ టూల్స్ డిఫైన్ చేద్దాం (Mock Tools)
def get_current_stock_price(ticker: str) -> str:
    prices = {"TCS": "₹3,950", "INFY": "₹1,620", "RELIANCE": "₹2,840"}
    ticker_clean = ticker.strip().upper()
    if ticker_clean in prices:
        return f"{ticker_clean} షేర్ ప్రస్తుత ధర: {prices[ticker_clean]}"
    return f"లోపం: {ticker_clean} టిక్కర్ కనుగొనబడలేదు."

def calculate_portfolio_value(units: int, price_per_unit: float) -> str:
    total = units * price_per_unit
    return f"మొత్తం పోర్ట్‌ఫోలియో విలువ: ₹{total:,.2f}"

TOOLS_REGISTRY = {
    "get_current_stock_price": get_current_stock_price,
    "calculate_portfolio_value": calculate_portfolio_value
}

# 2. Agent System Prompt (రూల్స్ మరియు ఫార్మాట్)
SYSTEM_PROMPT = """
నువ్వు స్టాక్ మార్కెట్ అసిస్టెంట్ ఏజెంట్‌వి.
నీకు ఈ కింది టూల్స్ అందుబాటులో ఉన్నాయి:
- get_current_stock_price(ticker): స్టాక్ ధరను ఇస్తుంది.
- calculate_portfolio_value(units, price_per_unit): మొత్తం విలువ లెక్కిస్తుంది.

నువ్వు ఖచ్చితంగా కింది ఫార్మాట్ మాత్రమే పాటించాలి:
Thought: <నువ్వు ఇప్పుడు ఏం చేయాలనుకుంటున్నావో ఆలోచించు>
Action: <tool_name>(<arguments>)
Observation: <టూల్ ఇచ్చిన ఫలితం ఇక్కడ కనిపిస్తుంది>
... (ఈ Thought/Action/Observation క్రమాన్ని అవసరమైనన్ని సార్లు రిపీట్ చేయొచ్చు)
Thought: నా దగ్గర ఫైనల్ సమాధానం ఉంది.
Final Answer: <యూజర్ కోసం పూర్తి తెలుగు సమాధానం>
"""

# 3. మాక్ LLM సిమ్యులేషన్ (ఇది వాస్తవంలో OpenAI/Gemini కి పంపబడుతుంది)
def mock_llm_response(prompt: str) -> str:
    # prompt చివర ఏముందో చూసి తదుపరి ఆలోచన లేదా సమాధానాన్ని జెనరేట్ చేస్తుంది
    if "Action:" not in prompt:
        return """Thought: నేను మొదట INFY స్టాక్ ప్రస్తుత ధర తెలుసుకోవాలి.
Action: get_current_stock_price("INFY")"""
    elif "INFY షేర్ ప్రస్తుత ధర: ₹1,620" in prompt and "calculate_portfolio_value" not in prompt:
        return """Thought: INFY ధర ₹1,620 అని తెలిసింది. ఇప్పుడు 50 షేర్ల విలువ లెక్కించాలి.
Action: calculate_portfolio_value(50, 1620)"""
    elif "మొత్తం పోర్ట్‌ఫోలియో విలువ: ₹81,000.00" in prompt:
        return """Thought: నా దగ్గర ఫైనల్ సమాధానం సిద్ధంగా ఉంది.
Final Answer: మీ 50 INFY షేర్ల మొత్తం విలువ ₹81,000 (ఒక్కో షేరు ధర ₹1,620)."""
    return "Final Answer: సమాచారం సరిపోలేదు."

# 4. ReAct Execution Loop (Agent Engine)
def run_agent_loop(user_query: str, max_iterations: int = 5):
    print(f"\n🚀 [USER QUERY]: {user_query}")
    history = SYSTEM_PROMPT + f"\nUser Query: {user_query}\n"
    
    for i in range(max_iterations):
        print(f"\n--- [Iteration {i+1}] ---")
        llm_output = mock_llm_response(history)
        print(llm_output)
        history += llm_output + "\n"
        
        # Final Answer వచ్చిందేమో చెక్ చేద్దాం
        if "Final Answer:" in llm_output:
            final_ans = llm_output.split("Final Answer:")[1].strip()
            print(f"\n🎉 [COMPLETE FINAL ANSWER]: {final_ans}")
            return final_ans
            
        # Action ని వెలికితీద్దాం (Regex)
        action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", llm_output)
        if action_match:
            tool_name = action_match.group(1)
            raw_args = action_match.group(2)
            
            # Arguments క్లీనింగ్
            args = [arg.strip().strip('"').strip("'") for arg in raw_args.split(",") if arg.strip()]
            
            print(f"🔧 [TOOL EXECUTION]: Calling {tool_name} with args {args}...")
            
            if tool_name in TOOLS_REGISTRY:
                func = TOOLS_REGISTRY[tool_name]
                # Type conversion (strings to int/float if needed)
                parsed_args = []
                for a in args:
                    try:
                        parsed_args.append(int(a) if a.isdigit() else float(a))
                    except ValueError:
                        parsed_args.append(a)
                
                tool_result = func(*parsed_args)
            else:
                tool_result = f"Error: Tool '{tool_name}' exists అవ్వలేదు."
                
            observation_str = f"Observation: {tool_result}"
            print(f"👁️ [{observation_str}]")
            history += observation_str + "\n"
        else:
            print("⚠️ యాక్షన్ ఫార్మాట్ మ్యాచ్ కాలేదు. లూప్ ముగింపు.")
            break
            
    print("❌ Max iterations రీచ్ అయింది.")

if __name__ == "__main__":
    run_agent_loop("నా దగ్గర 50 INFY షేర్లు ఉన్నాయి, వాటి మొత్తం విలువ ఎంత?")
```

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Fresher Pitfalls)

| తప్పు (Pitfall) | ఎందుకు జరుగుతుంది? | సరైన విధానం (Best Practice) |
| :--- | :--- | :--- |
| **ఇన్ఫినిట్ లూప్స్ (Infinite Loops)** | టూల్ ఒక ఎర్రర్ ఇస్తే ఏజెంట్ మళ్ళీ మళ్ళీ అదే టూల్ ని అదే పారామీటర్లతో పిలుస్తుంది. | ఖచ్చితంగా `max_iterations` (ఉదా: 5 లేదా 10) లిమిట్ పెట్టాలి. అలాగే ఎర్రర్ వచ్చినప్పుడు LLM కి "ఆల్టర్నేటివ్ ప్లాన్ చేయి" అని స్పష్టం చేయాలి. |
| **టూల్ కాల్స్ కి అన్-సేఫ్ `eval()` వాడటం** | LLM ఇచ్చిన స్ట్రింగ్ `get_price("TCS")` ని డైరెక్ట్ గా `eval()` చేయటం వలన ప్రాంప్ట్ ఇంజెక్షన్ సెక్యూరిటీ రిస్క్ వస్తుంది. | ఎప్పుడూ `JSON Function Calling` లేదా ప్రీ-డిఫైన్డ్ రిజిస్ట్రీ డిక్షనరీ మాత్రమే వాడాలి. |
| **లార్జ్ రెస్పాన్స్ తో కాంటెక్స్ట్ ఓవర్‌ఫ్లో** | టూల్ పెద్ద HTML పేజీని లేదా 10,000 రోస్ ఉన్న టేబుల్ ని అబ్జర్వేషన్ గా ఇస్తే కాంటెక్స్ట్ విండో అయిపోతుంది. | టూల్ ఫలితాన్ని ఏజెంట్ కి ఇచ్చేముందు సమ్మరైజ్ లేదా ట్రంకేట్ (Truncate) చేయాలి. |

---

## 7. ప్రాక్టికల్ ల్యాబ్ (Hands-on Lab)

### లక్ష్యం:
కస్టమర్ ఆర్డర్ స్టేటస్ మరియు రీఫండ్ ప్రాసెస్ చేయగల ఒక **Customer Support ReAct Agent** ని రూపొందించండి.

```python
# customer_agent_lab.py
import json

DATABASE = {
    "ORD-101": {"status": "DELIVERED", "item": "Wireless Headphones", "price": 1499},
    "ORD-102": {"status": "IN_TRANSIT", "item": "Mechanical Keyboard", "price": 3299}
}

def check_order(order_id: str) -> dict:
    order = DATABASE.get(order_id.upper())
    if order:
        return {"found": True, "order": order}
    return {"found": False, "error": "ఆర్డర్ నంబర్ దొరకలేదు."}

def initiate_refund(order_id: str, reason: str) -> dict:
    order_id = order_id.upper()
    if order_id not in DATABASE:
        return {"success": False, "message": "చెల్లని ఆర్డర్ ఐడీ."}
    if DATABASE[order_id]["status"] != "DELIVERED":
        return {"success": False, "message": "ఆర్డర్ డెలివరీ అవ్వకుండా రీఫండ్ సాధ్యం కాదు."}
    return {"success": True, "message": f"{order_id} కోసం ₹{DATABASE[order_id]['price']} రీఫండ్ అభ్యర్థన విజయవంతంగా నమోదైంది. కారణం: {reason}"}

# అభ్యాసం: ఈ రెండు టూల్స్ ని ఉపయోగించే Agent Controller ని మీరే రన్ చేసి టెస్ట్ చేయండి!
```

---

## 8. టాప్ 3 ఇంటర్వ్యూ ప్రశ్నలు & సమాధానాలు (Interview Q&A)

### Q1: LLM Function Calling కి మరియు ReAct Pattern కి తేడా ఏమిటి?
**సమాధానం:**
- **Function Calling:** ఇది మోడల్ (OpenAI/Gemini) ఇచ్చే ఒక స్ట్రక్చర్డ్ అవుట్‌పుట్ ఫీచర్. యూజర్ ప్రాంప్ట్ కి సరిపడే ఫంక్షన్ పేరు మరియు ఆర్గుమెంట్స్ ని JSON రూపంలో ఇస్తుంది.
- **ReAct Pattern:** ఇది ఒక ఆలోచనా ఫ్రేమ్‌వర్క్ (Design Pattern). ఇందులో మోడల్ కేవలం ఫంక్షన్ పిలవడమే కాకుండా, *"నేను ఈ ఫంక్షన్ ఎందుకు పిలుస్తున్నాను (Thought)"*, దాని ఫలితం చూసిన తర్వాత *"తదుపరి నా వ్యూహం ఏమిటి"* అని విశ్లేషిస్తూ పదే పదే లూప్ లో పనిచేస్తుంది. Function calling ని ReAct లో యాక్షన్ తీసుకోవడానికి ఒక సాధనంగా ఉపయోగిస్తారు.

### Q2: Agent హాలూసినేషన్ వల్ల తప్పుడు టూల్స్ పిలవకుండా ఎలా నియంత్రించవచ్చు?
**సమాధానం:**
1. **Pydantic Validation:** టూల్ కి వచ్చే ఇన్పుట్ పారామీటర్లను స్ట్రిక్ట్ టైప్స్ తో వాలిడేట్ చేయాలి.
2. **System Prompt Constraint:** ఏజెంట్ కి కేవలం అందుబాటులో ఉన్న టూల్స్ లిస్ట్ ఇచ్చి, అందులో లేనివి కనిపెట్టవద్దని హెచ్చరించాలి.
3. **Execution Guardrails:** ఏజెంట్ పిలిచిన టూల్ కోడ్ రిజిస్ట్రీ లో ఉందో లేదో వెరిఫై చేసి, లేకపోతే తిరిగి మోడల్ కి `"Invalid Tool Name"` అని స్పష్టమైన ఫీడ్‌బ్యాక్ ఇచ్చి లూప్ ని రీట్రై చేయించాలి.

### Q3: Autonomous AI Agent లో Memory యొక్క ప్రాముఖ్యత ఏమిటి?
**సమాధానం:**
ఏజెంట్ బహుళ-దశల (Multi-step) సమస్యలను పరిష్కరిస్తున్నప్పుడు, స్టెప్ 1 లో వచ్చిన ఫలితం స్టెప్ 4 లో అవసరం కావచ్చు. Short-term Memory (Chat Context) ద్వారా గత స్టెప్స్ లో చేసిన అబ్జర్వేషన్స్ గుర్తుంచుకుంటుంది. Long-term Memory (Vector Store) ద్వారా యూజర్ గతంలో ఇచ్చిన ప్రాధాన్యతలు మరియు గత టాస్క్ ల అనుభవాలను తిరిగి తెచ్చుకుని తప్పులు రిపీట్ కాకుండా చూసుకుంటుంది.
