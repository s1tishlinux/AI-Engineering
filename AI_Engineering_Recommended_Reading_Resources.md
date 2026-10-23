# AI Engineering: Curated Must-Read Substack Newsletters, Books & Core Resources 📚🤖

This curated guide collects the most authoritative, practical, and beginner-to-advanced learning materials across the global **AI Engineering** ecosystem (from Substack, O'Reilly books, top practitioner blogs, and engineering labs).

---

## 🌟 Top 8 AI Engineering Substacks & Newsletters

### 1. **Latent Space** (`latent.space`)
- **Authors:** Swyx (Shawn Wang) & Alessio Fanelli
- **Why It’s Essential:** Swyx coined the term and defined the role of the **"AI Engineer"**. This is the gold standard for understanding how software engineers are transitioning into AI application builders.
- **Top Must-Read Posts:**
  - *"The Rise of the AI Engineer"* — The seminal essay that created the discipline.
  - *"Reverse Prompt Engineering for Code Generation"*
  - *"AI Agents: From Tool Use to Autonomous Loops"*
- **Best For:** High-level trends, frontier lab interviews (Andrej Karpathy, George Hotz), and agent architectures.

---

### 2. **Ahead of AI** (`sebastianraschka.substack.com`)
- **Author:** Dr. Sebastian Raschka (Staff Research Engineer at Lightning AI, author of *Build a Large Language Model (From Scratch)*)
- **Why It’s Essential:** Extremely clear, visual, and zero-fluff explanations of how models actually work under the hood.
- **Top Must-Read Posts:**
  - *"Understanding Large Language Models: A Comprehensive Overview"*
  - *"Finetuning LLMs: LoRA, QLoRA, and Full Finetuning Explained with Code"*
  - *"Evaluating LLM Output Quality: Best Practices"*
- **Best For:** Freshers who want the intuition and math made simple with runnable Python code.

---

### 3. **Hamel's Substack** (`hamel.substack.com` & `hamel.dev`)
- **Author:** Hamel Husain (Former ML engineer at GitHub, Airbnb, DataRobot)
- **Why It’s Essential:** The industry's leading authority on **LLM Evaluations (Evals)**, data flywheels, and moving from prototype to reliable production.
- **Top Must-Read Posts:**
  - *"Your AI Product Needs Evals"* — The definitive guide on why vibes-based testing fails.
  - *"Creating A LLM as a Judge That You Can Trust"*
  - *"How to Build an Agent that Doesn't Hallucinate"*
- **Best For:** MLOps, LLMOps, real-world evaluation pipelines, and debugging agent failure modes.

---

### 4. **Eugene Yan's Applied AI Blog** (`eugeneyan.com` & Substack archive)
- **Author:** Eugene Yan (Member of Technical Staff at Anthropic, ex-Amazon, ex-Lazada)
- **Why It’s Essential:** The most referenced playbook for practical software patterns in generative AI and recommender systems.
- **Top Must-Read Posts:**
  - *"Patterns for Building LLM-based Systems & Products"* (A multi-million view masterclass).
  - *"Evaluation & Monitoring of LLM Applications"*
  - *"RAG vs Fine-tuning: When to Use What"*
- **Best For:** System architecture, RAG design patterns, and enterprise AI production readiness.

---

### 5. **ByteByteGo Newsletter** (`bytebytego.substack.com`)
- **Authors:** Alex Xu & the ByteByteGo Engineering Team
- **Why It’s Essential:** Incredible visual system design diagrams that explain complex distributed systems, vector databases, and AI pipelines in 5 minutes.
- **Top Must-Read Posts:**
  - *"How Vector Databases Work (Under the Hood)"*
  - *"System Design: Building a Production-Scale RAG Pipeline"*
  - *"Understanding Transformer Architecture in One Visual Diagram"*
- **Best For:** Visual learners and freshers preparing for System Design & AI Architecture interviews.

---

### 6. **Interconnects** (`interconnects.ai`)
- **Author:** Nathan Lambert (Research Scientist at Allen Institute for AI - AI2)
- **Why It’s Essential:** Deep analysis of the research-to-engineering frontier: RLHF, DPO, post-training, and open-source models (Llama, Mistral, Olmo).
- **Best For:** Understanding why models behave the way they do after pre-training and alignment.

---

### 7. **The Sequence** (`thesequence.substack.com`)
- **Author:** Jesus Rodriguez
- **Why It’s Essential:** Concise 5-minute breakdowns of every milestone research paper, new agent framework, and cloud AI release published every week.
- **Best For:** Staying up to date with new foundational model releases without drowning in academic jargon.

---

### 8. **AI Engineering Insider** (`aiengineeringinsider.substack.com`)
- **Author:** Practical engineering community contributors
- **Focus:** System design interview prep, API integration guides, and hands-on Python agent implementations for engineering teams.

---

## 📖 The 4 Essential AI Engineering Books Every Fresher Should Read

| Book Title | Author | Publisher | Why You Should Read It |
| :--- | :--- | :--- | :--- |
| **AI Engineering: Building Applications with Foundation Models** | Chip Huyen | O'Reilly (2025) | The Bible of AI Engineering. Covers training vs fine-tuning, latency optimization, RAG, agents, caching, and evaluation. |
| **Build a Large Language Model (From Scratch)** | Sebastian Raschka | Manning (2024/2025) | Walks through coding a GPT-style transformer line-by-line in pure PyTorch. The best book to demystify tokens, attention, and weights. |
| **Designing Machine Learning Systems** | Chip Huyen | O'Reilly (2022) | Foundational MLOps: Data pipelines, feature stores, drift detection, and automated retraining. |
| **System Design Interview – An Insider's Guide (Volume 2)** | Alex Xu & Sahn Lam | ByteByteGo | Teaches how to scale distributed systems, microservices, and databases to millions of requests. |

---

## 🛠️ Essential Official Engineering Guides & Cookbooks

1. **Anthropic Engineering Blog: *"Building Effective Agents"***
   - *URL:* `anthropic.com/research/building-effective-agents`
   - *Key takeaway:* Simple workflows (Prompt Chaining, Routing, Parallelization) beat complicated, chaotic autonomous loops 90% of the time.
2. **OpenAI Cookbook**
   - *URL:* `github.com/openai/openai-cookbook`
   - Hundreds of runnable Python scripts on structured outputs, function calling, vector embeddings, and token cost optimization.
3. **Google Gemini API Documentation & Cookbook**
   - *URL:* `github.com/google-gemini/cookbook`
   - Native multimodal recipes (video ingestion, audio analysis, 2M token context handling).
4. **LangChain & LangGraph Tutorials**
   - *URL:* `langchain-ai.github.io/langgraph`
   - Interactive guides on state machines, human-in-the-loop pauses, and multi-agent coordination.

---

## 💡 How to Integrate These Resources Into Your 40-Day Curriculum

| 40-Day Curriculum Module | Recommended Complementary Substack / Book Reading |
| :--- | :--- |
| **Module 04: AI & ML Foundations** | *Ahead of AI* (Sebastian Raschka) + *Build a Large Language Model (From Scratch)* |
| **Module 05: Generative AI & LLMs** | *Latent Space* ("Rise of the AI Engineer") + *ByteByteGo* ("Visual Guide to Transformers") |
| **Module 06: RAG & Applications** | Eugene Yan's *"Patterns for Building LLM Systems"* + ByteByteGo *"Production RAG Design"* |
| **Module 07: Agentic AI & MCP** | Anthropic's *"Building Effective Agents"* + Latent Space episodes on Model Context Protocol |
| **Module 08: MLOps & LLMOps** | Hamel Husain's *"Your AI Product Needs Evals"* + Chip Huyen's *AI Engineering* (Chapters on Evaluation & Drift) |
| **Module 09: Cloud Computing for AI** | ByteByteGo on Cloud Scalability + Official AWS Bedrock/GCP Vertex AI Cookbooks |
