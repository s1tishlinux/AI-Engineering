# Day 35: LLMOps, Observability & Evaluation (Ragas & Tracing) 🔍

---

## 1. Day 35 Learning Objectives
- Understand why traditional ML metrics (Accuracy, F1-score) fail when evaluating non-deterministic Generative AI and LLM outputs.
- Master the **RAG Triad** of metrics: **Faithfulness / Groundedness**, **Answer Relevance**, and **Context Recall/Precision**.
- Instrument automated **LLM Tracing & Observability** (OpenInference, Langfuse, MLflow Tracing) to record latency, token spend, prompts, and retrieval chunks for every production query.
- Manage **Prompt Versioning** as code artifacts instead of hardcoded strings scattered across business logic.
- Implement automated LLM-as-a-Judge evaluation pipelines to catch hallucinations before users report them.

---

## 2. Real-World Analogy

> 💡 **Analogy: Multiple-Choice Exam Grading vs. Evaluating a Legal Essay**
>
> - **Traditional MLOps (Multiple-Choice Exam):**
>   Grading a classic classification model is like checking a bubble sheet. Question 1: Is it option B? If yes, 100%. If no, 0%. It is black-and-white, instantaneous, and mathematically exact.
> - **LLMOps (Evaluating a Legal Argument or Medical Summary):**
>   An LLM produces a 300-word summary of a medical diagnosis. You cannot check if word #14 matches a reference string.
>   Instead, you need a senior expert (or an automated **LLM-as-a-Judge**) to read the essay and grade:
>   1. **Faithfulness:** Did the student invent facts not present in the medical textbook? (Hallucination check)
>   2. **Answer Relevance:** Did the student actually answer the patient's specific question?
>   3. **Context Recall:** Did the student miss any critical contraindication mentioned in the patient's chart?

---

## 3. Architecture Overview: The LLMOps Observability & Evaluation Stack

```
                     ┌──────────────────────────────┐
                     │          USER PROMPT         │
                     └──────────────┬───────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        LLM APPLICATION PIPELINE                        │
│                                                                        │
│   Step 1: Retrieve Context Chunks (Vector DB)                          │
│   Step 2: Format Versioned Prompt Template                             │
│   Step 3: Call LLM API (OpenAI / Claude / Gemini)                      │
│   Step 4: Return Streamed Response                                     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Emits Trace Span Events
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   OBSERVABILITY & EVALUATION ENGINE                    │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │     TRACING / TELEMETRY   │      │    EVALUATION (RAG TRIAD)   │   │
│   │ - Latency per step        │      │ 1. Faithfulness Score       │   │
│   │ - Input & Output Tokens   │      │ 2. Answer Relevance Score   │   │
│   │ - Cost per request ($)    │      │ 3. Context Relevance Score  │   │
│   └───────────────────────────┘      └─────────────────────────────┘   │
│                                                                        │
│   Alerting & Feedback Loop:                                            │
│   - If Faithfulness < 0.85 -> Trigger Slack Alert / Route to Human     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. The Core LLM Evaluation Metrics (The RAG Triad)

1. **Faithfulness (Groundedness):**
   - *Question:* Is every factual claim in the generated answer supported by the retrieved context?
   - *Catches:* Hallucinations and fabricated information.
2. **Answer Relevance:**
   - *Question:* Does the generated response directly answer the user's specific query, without drifting into irrelevant fluff?
   - *Catches:* Evasive answers, off-topic rambling, or incomplete responses.
3. **Context Precision & Recall:**
   - *Question:* Did the vector search retrieve the actual ground-truth facts needed to answer the prompt, and was noise minimized?
   - *Catches:* Bad chunking, poor embeddings, or weak search algorithms.

---

## 5. Coding Walkthrough: LLM-as-a-Judge Faithfulness Evaluator

Here is a pure Python implementation of an automated **LLM-as-a-Judge** scoring engine that calculates the Faithfulness score of an LLM response against retrieved context chunks:

```python
# evaluate_faithfulness.py
"""
Production Faithfulness & Groundedness Evaluator
Calculates: Supported Claims / Total Claims
"""
import json
import re
from typing import List, Dict

# Mock LLM API call simulating an evaluation judge (e.g. GPT-4 or Claude 3.5 Sonnet)
def mock_llm_judge_call(prompt: str) -> str:
    """Simulates LLM-as-a-Judge reasoning."""
    if "Extract all atomic factual claims" in prompt:
        return json.dumps({
            "claims": [
                "Python was created by Guido van Rossum.",
                "Python was released in 1991.",
                "Python is primarily designed for compiled C execution." # Fabricated claim!
            ]
        })
    elif "Verify if the claim is supported" in prompt:
        # Evaluates each claim against context
        return json.dumps({
            "verification": [
                {"claim": "Python was created by Guido van Rossum.", "supported": True, "reason": "Mentioned explicitly in text."},
                {"claim": "Python was released in 1991.", "supported": True, "reason": "Mentioned explicitly in text."},
                {"claim": "Python is primarily designed for compiled C execution.", "supported": False, "reason": "Context states Python is an interpreted language."}
            ]
        })
    return "{}"

class FaithfulnessEvaluator:
    def evaluate(self, answer: str, context: str) -> Dict[str, any]:
        # Step 1: Claim Extraction Prompt
        prompt_extract = f"""
        Extract all atomic factual claims made in this generated answer:
        Answer: {answer}
        Return JSON with key 'claims': list of strings.
        """
        extract_res = json.loads(mock_llm_judge_call(prompt_extract))
        claims = extract_res.get("claims", [])
        
        if not claims:
            return {"score": 1.0, "total_claims": 0, "supported_claims": 0, "verifications": []}

        # Step 2: Verification against retrieved Context
        prompt_verify = f"""
        Given the Context:
        {context}
        Verify if the claim is supported by the context.
        Claims to verify: {claims}
        Return JSON with key 'verification': list of objects with 'claim', 'supported', and 'reason'.
        """
        verify_res = json.loads(mock_llm_judge_call(prompt_verify))
        verifications = verify_res.get("verification", [])

        # Step 3: Compute Mathematical Faithfulness Score
        supported_count = sum(1 for v in verifications if v.get("supported") is True)
        total_count = len(verifications)
        score = supported_count / total_count if total_count > 0 else 0.0

        return {
            "faithfulness_score": round(score, 4),
            "total_claims": total_count,
            "supported_claims": supported_count,
            "hallucination_detected": score < 1.0,
            "verifications": verifications
        }

if __name__ == "__main__":
    retrieved_context = (
        "Python is an interpreted, high-level programming language created by "
        "Guido van Rossum and first released in 1991. It emphasizes code readability."
    )
    
    generated_answer = (
        "Python was created by Guido van Rossum and released in 1991. "
        "It is primarily designed for compiled C execution."
    )
    
    evaluator = FaithfulnessEvaluator()
    results = evaluator.evaluate(answer=generated_answer, context=retrieved_context)
    
    print("\n--- LLMOps Evaluation Results ---")
    print(f"Faithfulness Score : {results['faithfulness_score'] * 100:.1f}%")
    print(f"Total Claims Found : {results['total_claims']}")
    print(f"Supported Claims   : {results['supported_claims']}")
    print(f"Hallucination Flag : {'🚨 YES' if results['hallucination_detected'] else '✅ NO'}")
    print("\nDetailed Claim Breakdown:")
    for v in results["verifications"]:
        status = "✅ PASS" if v["supported"] else "❌ HALLUCINATED"
        print(f"[{status}] {v['claim']}")
        print(f"   Reason: {v['reason']}")
```

---

## 6. Common Fresher Pitfalls

| Pitfall | Why It Causes Production Failure | Best Practice |
| :--- | :--- | :--- |
| **Evaluating LLMs with Exact String Match / BLEU** | Natural language answers can be completely factual and helpful while using completely different synonyms. BLEU scores punish valid rephrasing. | Use semantic evaluation (Cosine similarity on embeddings) or structured LLM-as-a-Judge prompting. |
| **No Production Tracing / Logging** | When a customer complains about a bad LLM response, the engineering team cannot inspect which retrieved chunks or prompt caused the mistake. | Implement structured distributed tracing (Langfuse, OpenTelemetry) capturing `input_prompt`, `retrieved_chunks`, `latency_ms`, and `completion`. |
| **Hardcoding Prompts in Code Files** | Embedding prompts in Python string variables prevents prompt engineers from testing, updating, or versioning prompts without redeploying code. | Store prompts in versioned prompt registries (YAML files, MLflow Prompts, or Langfuse prompt repositories). |

---

## 7. Hands-on Lab: Instrumenting Request Latency & Token Spend

### Objective:
Build an observability wrapper function that measures and logs:
1. End-to-end execution time in milliseconds.
2. Estimated token count and cost ($0.0015 per 1K input tokens, $0.002 per 1K output tokens).

```python
# lab_day35_observability.py
import time

def track_llm_call(prompt: str, mock_completion: str):
    start_time = time.perf_counter()
    
    # Simulate LLM inference delay
    time.sleep(0.15)
    
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    # Token estimation (rule of thumb: ~4 characters per token)
    input_tokens = len(prompt) // 4
    output_tokens = len(mock_completion) // 4
    
    cost_input = (input_tokens / 1000.0) * 0.0015
    cost_output = (output_tokens / 1000.0) * 0.0020
    total_cost = cost_input + cost_output
    
    trace = {
        "latency_ms": round(elapsed_ms, 2),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_cost_usd": f"${total_cost:.6f}"
    }
    print("Trace Event Logged:", trace)
    return trace

track_llm_call("Explain quantum computing in 1 sentence.", "Quantum computing uses qubits to process complex states.")
```

---

## 8. Top 3 Interview Questions & Answers

### Q1: What is the "RAG Triad" and why is it preferred over human manual review?
**Answer:**
The RAG Triad consists of three automated, objective metrics: **Faithfulness** (does the answer contain facts not in the context?), **Answer Relevance** (does the answer address the question?), and **Context Precision/Recall** (did retrieval fetch the right documents?). Manual human review is too slow, expensive, and subjective to evaluate thousands of queries per day. The RAG Triad enables automated regression testing in CI/CD and continuous production monitoring.

### Q2: How does the "LLM-as-a-Judge" paradigm work, and what are its potential biases?
**Answer:**
LLM-as-a-Judge uses a powerful foundational model (e.g., GPT-4) guided by a rigorous rubric to evaluate outputs generated by smaller or domain-specific models.
While effective, judges can suffer from:
1. **Position Bias:** Preferring the first candidate presented in a comparison.
2. **Verbosity Bias:** Favoring longer, more wordy responses even if less concise.
3. **Self-Enhancement Bias:** Giving higher scores to responses generated by models from the same model family.

### Q3: Why is Tracing essential in an Agentic / RAG architecture?
**Answer:**
In multi-step systems (e.g., LangGraph or agentic loops), an end-to-end user request involves multiple vector search calls, tool invocations, and LLM completions. If the final answer is wrong or slow, simple logging cannot identify which specific step failed. Tracing groups all sub-steps under a single `Trace ID`, visualizing the exact latency, token usage, and payload at every node in the execution graph.
