# Day 21: Generative AI & Large Language Model Foundations

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The paradigm shift: Predictive ML vs **Generative AI**.
2. How Foundation Models work: Pretraining (Next-Token Prediction) $\rightarrow$ Instruction Tuning $\rightarrow$ RLHF.
3. The modern foundation model landscape: **Proprietary** (Gemini 1.5, GPT-4o, Claude 3.5) vs **Open-Weight** (Llama 3, Mistral, Gemma).
4. Anatomy of Context Windows (32k to 2 Million tokens) and the Needle-in-a-Haystack problem.
5. Hyperparameters that control generation: **Temperature**, **Top-p (Nucleus Sampling)**, and **Top-k**.

---

## 1. The "Why": The Autoregressive Engine

Traditional ML (predictive) outputs a label or a number:
- `Is this email spam? -> 1 (Spam)`
- `What is the house price? -> ₹75 Lakhs`

Generative AI produces **brand new, coherent artifacts** (prose, SQL queries, Python scripts, JSON schemas).
At its core, every Large Language Model is simply an **extremely sophisticated Next-Token Prediction engine**:

```
Given the prompt: "The capital of India is"
Model computes probabilities across 100,000 tokens:
  - "New"    : 92.4%  <── Highest Probability!
  - "Delhi"  :  4.1%
  - "Mumbai" :  1.2%
The model picks "New", appends it to the prompt, and predicts the next token: "Delhi"!
```

---

## 2. How LLMs are Built: The 3-Stage Training Pipeline

Understanding this lifecycle is crucial for every fresher interview:

```
┌─────────────────────────────────┐
│ 1. PRETRAINING (Raw Base Model) │  Web Scrape (Trillions of tokens), Months on 10,000+ GPUs
│ Learns grammar, facts, & world  │  Predicts next word. (Will complete a prompt, but cannot chat!)
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│ 2. SUPERVISED FINE-TUNING (SFT) │  High-quality question-answer pairs curated by humans
│ Learns to follow instructions   │  Becomes an "Instruct" model (e.g. Llama-3-Instruct)
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│ 3. RLHF / DPO (Alignment)       │  Reinforcement Learning from Human Feedback
│ Safety, helpfulness, & tone     │  Prevents dangerous outputs (weapons, malware, hate speech)
└─────────────────────────────────┘
```

---

## 3. The Model Landscape: Closed vs Open-Weight

| Category | Top Models | Strengths | Tradeoffs |
| :--- | :--- | :--- | :--- |
| **Proprietary (API-Only)** | Google Gemini 1.5 Pro, OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet | State-of-the-art reasoning, massive context (Gemini: 2M tokens), multimodal native | Recurring API cost per token, proprietary weights, data leaves perimeter |
| **Open-Weight (Self-Hosted)** | Meta Llama 3.1 (8B, 70B, 405B), Mistral NeMo, Google Gemma 2 | Complete privacy, zero per-token cost, runs on private on-prem GPUs, full weight access | Requires heavy GPU infrastructure (H100/A100) or local quantized runtimes |

---

## 4. Context Windows: The Short-Term Working Memory

- **Context Window**: The maximum number of tokens an LLM can perceive in a single interaction (combining system instructions, conversation history, retrieved documents, and the generated response).
  - GPT-3.5 (2022): 4,096 tokens (~3 pages)
  - Claude 3.5 (2024): 200,000 tokens (~150 pages)
  - Google Gemini 1.5 Pro (2024+): **2,000,000 tokens** (1 hour of video, 60,000 lines of code, or 1,500 pages of text!).
- **The "Lost in the Middle" Phenomenon**: Models pay most attention to tokens at the very beginning and very end of the context window. Information buried in the exact middle is sometimes overlooked.

---

## 5. Inference Hyperparameters (Controlling the Creativity Valve)

```python
# The 3 critical dials on every LLM generation request:
generation_config = {
    # 1. Temperature (0.0 to 2.0)
    # 0.0 = Deterministic, strictly picks highest probability token. (Best for Code & JSON!)
    # 0.7 = Balanced (Default for conversational chatbots)
    # 1.5 = Wild, creative, unpredictable (Poetry, brainstorming)
    "temperature": 0.2,

    # 2. Top-P (Nucleus Sampling)
    # Considers only the smallest pool of tokens whose cumulative probability exceeds P.
    # Top-p = 0.9 ignores the bottom 10% bizarre or nonsensical tokens.
    "top_p": 0.95,

    # 3. Top-K
    # Strictly limits the candidate pool to the top K most probable words.
    "top_k": 40
}
```

---

## 6. Common Fresher Pitfalls

1. **Setting high temperature for code or JSON generation**:
   - Setting `temperature=1.2` when expecting valid JSON guarantees syntax errors and hallucinated keys. For JSON, SQL, or code, always set `temperature=0.0` or `0.1`!
2. **Confusing Context Window with Long-Term Memory**:
   - The context window is volatile RAM. The moment a session ends or exceeds context, the LLM forgets everything unless saved to a database.
3. **Assuming LLMs can "search the live web" by default**:
   - Base LLMs are frozen in time at their training cutoff date. To access live data, they must be augmented with Tools (Function Calling) or RAG.

---

## 7. Daily Hands-On Lab

### 🧪 Exercise: Build an Interactive Generation Parameter Playground
**Scenario**: Simulate how varying `temperature` flattens or sharpens the token probability distribution, showing mathematically why high temperature breeds creativity and low temperature yields strict predictability.

```python
# =========================================================
# Day 21 Lab: Temperature & Softmax Probability Simulator
# =========================================================
import numpy as np

def simulate_llm_token_sampling(logits: dict[str, float], temperature: float = 1.0) -> dict[str, float]:
    tokens = list(logits.keys())
    raw_scores = np.array(list(logits.values()))

    # Apply Temperature scaling (prevent division by exact zero)
    temp = max(temperature, 1e-4)
    scaled_scores = raw_scores / temp

    # Softmax conversion to probabilities
    exp_scores = np.exp(scaled_scores - np.max(scaled_scores))  # Numerical stability trick
    probabilities = exp_scores / np.sum(exp_scores)

    return {token: np.round(prob * 100, 2) for token, prob in zip(tokens, probabilities)}

# Candidate next tokens for: "The programmer debugged the code and found a _____"
candidate_logits = {
    "bug": 8.5,       # Most expected
    "typo": 6.2,      # Plausible
    "syntax_error": 5.8,
    "sandwich": 1.2,  # Bizarre outlier
    "dragon": 0.5     # Wild hallucination
}

print("="*60)
print("LLM INFERENCE SAMPLING SIMULATION")
print("="*60)

for temp in [0.1, 0.7, 1.5]:
    probs = simulate_llm_token_sampling(candidate_logits, temperature=temp)
    print(f"\n🌡️ Temperature = {temp}:")
    for token, percentage in sorted(probs.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(percentage // 3)
        print(f"  • {token:15}: {percentage:5.1f}% | {bar}")
print("="*60)
```

---

## 8. Interview Quick-Fire Questions

1. **Q: What is the difference between Pretraining and Fine-Tuning in LLMs?**
   - **Answer**: **Pretraining** is self-supervised learning on massive internet-scale text corpora (trillions of tokens) where the model learns language structure and world knowledge via next-token prediction; it is computationally immense (millions of dollars). **Fine-Tuning** takes a pretrained base model and trains it on a smaller, curated dataset (e.g. instruction pairs or medical records) to specialize its behavior, style, or task execution at a fraction of the cost.
2. **Q: What is Hallucination in Large Language Models and why does it occur?**
   - **Answer**: Hallucination occurs when an LLM generates factually false or nonsensical statements with high linguistic confidence. It happens because LLMs are probabilistic token predictors optimizing for grammatical fluency and coherence, not verified truth retrieval engines.
3. **Q: How does Top-P (Nucleus Sampling) differ from Top-K sampling?**
   - **Answer**: **Top-K** strictly selects a fixed number ($K$) of the highest-probability tokens, regardless of the probability distribution shape. **Top-P** dynamically selects a variable number of tokens whose cumulative probability reaches threshold $P$ (e.g. 0.9), expanding the candidate pool when many tokens are viable and contracting it when one token is overwhelmingly dominant.
