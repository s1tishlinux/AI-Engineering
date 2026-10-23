# Day 07: Advanced OOP (Inheritance, Polymorphism & Abstraction)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. **Inheritance**: Code reuse by establishing an "IS-A" parent-child relationship.
2. **Polymorphism**: The ability of different classes to respond to the same method call with custom behavior.
3. **Abstraction & Interfaces**: Enforcing contracts using the `abc` (Abstract Base Class) module.
4. **Composition over Inheritance**: Building modular systems via "HAS-A" relationships.
5. **Multiple Inheritance & MRO** (Method Resolution Order) and `super()`.

---

## 1. The "Why": Building Extensible AI Systems

In enterprise software and modern AI architectures (such as LangChain, LlamaIndex, or PyTorch), you rarely build a single monolithic class. Instead, you design extensible interfaces:
- An abstract `BaseLLM` interface with a `.generate(prompt)` contract.
- Concrete children: `OpenAILLM`, `GeminiLLM`, `AnthropicLLM`, and `LocalOllamaLLM`.
- Your application interacts with `BaseLLM`, so swapping OpenAI for Gemini requires changing **one line of configuration**, not rewriting your entire app!

---

## 2. Abstraction with `abc.ABC` & `@abstractmethod`

An **Abstract Class** cannot be instantiated directly. It acts as a strict contract that guarantees every child class implements specific required methods.

```python
from abc import ABC, abstractmethod

# The Contract / Interface
class NotificationService(ABC):
    @abstractmethod
    def send_alert(self, recipient: str, message: str) -> bool:
        """All notification services MUST implement this method."""
        pass

# ❌ TypeError: Can't instantiate abstract class NotificationService with abstract method send_alert
# service = NotificationService()

# Concrete Implementation 1: Email
class EmailNotification(NotificationService):
    def send_alert(self, recipient: str, message: str) -> bool:
        print(f"📧 [EMAIL SENT to {recipient}]: {message}")
        return True

# Concrete Implementation 2: Slack Webhook
class SlackNotification(NotificationService):
    def send_alert(self, recipient: str, message: str) -> bool:
        print(f"💬 [SLACK POSTED to channel #{recipient}]: {message}")
        return True
```

---

## 3. Polymorphism in Action

**Polymorphism** means "many forms". It allows a single function to process different objects uniformly, provided they share the same interface.

```python
def broadcast_security_breach(services: list[NotificationService], target: str, incident: str):
    """Notice how this function doesn't care whether it is Email, Slack, or SMS!"""
    for service in services:
        service.send_alert(target, f"🚨 ALERT: {incident}")

# Testing Polymorphism
channels = [EmailNotification(), SlackNotification()]
broadcast_security_breach(channels, "devops-team", "Unauthorized API access detected on Port 8080")
```

---

## 4. `super()` & Method Overriding

When a child class needs to extend (rather than replace) the behavior of its parent class, `super()` delegates calls to the parent implementation.

```python
class CloudResource:
    def __init__(self, resource_id: str, region: str):
        self.resource_id = resource_id
        self.region = region

    def get_info(self) -> str:
        return f"Resource: {self.resource_id} | Region: {self.region}"

class VirtualMachine(CloudResource):
    def __init__(self, resource_id: str, region: str, cpu_cores: int, ram_gb: int):
        # Call the parent constructor using super()
        super().__init__(resource_id, region)
        self.cpu_cores = cpu_cores
        self.ram_gb = ram_gb

    # Method Overriding: Specialize the parent's get_info()
    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info} | Specs: {self.cpu_cores} vCPU, {self.ram_gb} GB RAM"

vm = VirtualMachine("vm-ai-train-01", "ap-south-1 (Mumbai)", cpu_cores=16, ram_gb=64)
print(vm.get_info())
```

---

## 5. Composition vs Inheritance: "Favor Composition"

One of the most critical design principles in software engineering:
- **Inheritance ("IS-A")**: A Dog *is an* Animal. (Tight coupling — changing parent breaks children).
- **Composition ("HAS-A")**: A Car *has an* Engine. A Computer *has a* GPU. (Loose coupling, flexible swapping).

```python
# ==========================================
# Composition Example: Modern AI Agent
# ==========================================

class VectorDatabase:
    def search(self, query: str):
        return f"[Vector Results for '{query}']"

class LLMBrain:
    def think(self, context: str):
        return f"Generated answer based on {context}"

class AutonomousAgent:
    """Agent HAS-A VectorDatabase and HAS-A LLMBrain."""
    def __init__(self, memory: VectorDatabase, brain: LLMBrain):
        self.memory = memory  # Composed dependency
        self.brain = brain    # Composed dependency

    def execute_task(self, query: str):
        context = self.memory.search(query)
        response = self.brain.think(context)
        return response

# You can swap out vector databases or LLMs anytime without touching AutonomousAgent!
agent = AutonomousAgent(VectorDatabase(), LLMBrain())
print(agent.execute_task("Explain Transformers"))
```

---

## 6. Multiple Inheritance & Method Resolution Order (MRO)

Python allows a class to inherit from multiple parent classes. Python resolves method names using the **C3 Linearization Algorithm** (viewed via `.mro()`).

```python
class LoggerMixin:
    def log(self, message):
        print(f"[LOG]: {message}")

class ValidatorMixin:
    def validate(self, data):
        print(f"[VALIDATE]: Checking schema for {data}")

class DataIngestionPipeline(LoggerMixin, ValidatorMixin):
    def run(self, payload):
        self.validate(payload)
        self.log("Ingesting data to BigQuery...")

pipeline = DataIngestionPipeline()
pipeline.run({"record_count": 500})

# Inspecting MRO
print("MRO Order:", [cls.__name__ for cls in DataIngestionPipeline.mro()])
```

---

## 7. Common Fresher Pitfalls

1. **Deep Inheritance Trees**:
   - Creating 5 levels of inheritance (`Animal -> Mammal -> Carnivore -> Canine -> Dog`) leads to the "Fragile Base Class" anti-pattern. Keep inheritance trees shallow (maximum 2 levels).
2. **Forgetting to implement abstract methods**:
   - If a subclass omits even one `@abstractmethod`, attempting to instantiate the subclass raises a `TypeError` at runtime.
3. **Violating Liskov Substitution Principle (LSP)**:
   - If class `B` inherits from `A`, substituting `B` wherever `A` is expected should never break the program.

---

## 8. Daily Hands-On Lab

### 🧪 Exercise: Multi-Provider AI Model Client Interface
**Scenario**: You are designing an AI Gateway for your company. Create an abstract base class `BaseAIProvider` and concrete implementations for `OpenAIProvider` and `GeminiProvider`.

```python
# ==========================================
# Day 7 Lab: Multi-Cloud AI Gateway
# ==========================================
from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    def __init__(self, api_key: str, model_id: str):
        self.api_key = api_key
        self.model_id = model_id

    @abstractmethod
    def generate_completion(self, prompt: str) -> dict:
        """Returns structured dictionary with response text and tokens."""
        pass

class GeminiProvider(BaseAIProvider):
    def generate_completion(self, prompt: str) -> dict:
        # Simulated Gemini API call
        response_text = f"✨ [Gemini {self.model_id}]: Analyzed prompt: '{prompt[:30]}...'"
        return {
            "provider": "Google Vertex AI / Gemini",
            "model": self.model_id,
            "response": response_text,
            "tokens_consumed": len(prompt) // 3
        }

class OpenAIProvider(BaseAIProvider):
    def generate_completion(self, prompt: str) -> dict:
        # Simulated OpenAI API call
        response_text = f"🤖 [OpenAI {self.model_id}]: Response for: '{prompt[:30]}...'"
        return {
            "provider": "OpenAI",
            "model": self.model_id,
            "response": response_text,
            "tokens_consumed": len(prompt) // 4
        }

class EnterpriseAIGateway:
    """Routes requests to the selected provider using Polymorphism."""
    def __init__(self, provider: BaseAIProvider):
        self.provider = provider

    def query(self, prompt: str):
        print(f"\nRouting query via {self.provider.__class__.__name__}...")
        result = self.provider.generate_completion(prompt)
        print(f"Result : {result['response']}")
        print(f"Tokens : {result['tokens_consumed']}")

# Test swapping providers seamlessly
gemini_client = GeminiProvider(api_key="AIzaSyDummyKey", model_id="gemini-1.5-pro")
openai_client = OpenAIProvider(api_key="sk-proj-DummyKey", model_id="gpt-4o")

gateway = EnterpriseAIGateway(gemini_client)
gateway.query("How do attention heads work in Transformers?")

# Seamlessly switch provider
gateway.provider = openai_client
gateway.query("How do attention heads work in Transformers?")
```

---

## 9. Interview Quick-Fire Questions

1. **Q: What is the purpose of Python's `abc` module?**
   - **Answer**: The `abc` (Abstract Base Class) module provides the infrastructure for defining formal interfaces in Python. Decorating a method with `@abstractmethod` forces any subclass to implement that method before it can be instantiated.
2. **Q: Why is Composition often preferred over Inheritance?**
   - **Answer**: Inheritance creates a tight, fragile coupling between parent and child classes ("IS-A"). Composition creates loose coupling ("HAS-A") by assembling independent objects together, making the system easier to test, refactor, and swap implementations at runtime.
3. **Q: How does Python resolve method names in multiple inheritance?**
   - **Answer**: Python uses the **C3 Linearization Algorithm** to construct the **Method Resolution Order (MRO)**, traversing base classes from left to right in a deterministic, monotonic order without duplicate evaluations.
