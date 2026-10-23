# Day 25: LLM Customization (Prompting vs RAG vs Fine-Tuning & LoRA)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The Architectural Decision Matrix: When to choose **Prompt Engineering** vs **RAG** vs **Fine-Tuning**.
2. **Supervised Fine-Tuning (SFT)** data pipelines (JSONL instruction formats).
3. Parameter-Efficient Fine-Tuning (**PEFT**) and **LoRA (Low-Rank Adaptation)** mechanics.
4. **Model Quantization**: FP16 $\rightarrow$ INT8 $\rightarrow$ INT4 (GGUF, AWQ, and QLoRA).
5. Selecting the right foundation model size (7B vs 70B) for enterprise latency and cost requirements.

---

## 1. The Decision Matrix: Prompting vs RAG vs Fine-Tuning

Freshers frequently make the fatal mistake of jumping straight into expensive Fine-Tuning when a simple prompt or RAG would have worked better!

```
                  DO YOU NEED EXTERNAL / NEW KNOWLEDGE?
                             /               \
                           YES                NO
                           /                   \
                  Use RAG (Module 06)    DO YOU NEED TO CHANGE
                  (Live docs, DBs,       STYLE, TONE, OR SYNTAX?
                   proprietary manuals)        /            \
                                             YES             NO
                                             /                \
                                        FINE-TUNING      PROMPT ENGINEERING
                                        (LoRA / SFT)     (System Prompts, Few-Shot)
```

| Dimension | Prompt Engineering | Retrieval-Augmented Generation (RAG) | Fine-Tuning (LoRA / SFT) |
| :--- | :--- | :--- | :--- |
| **Best For** | Quick prototyping, general tasks | Live knowledge, company documents, citations | Specialized tone, obscure JSON syntax, niche jargon |
| **Data Requirements** | 0 to 5 examples | Vectorized knowledge base | 500 to 10,000+ curated pairs |
| **Cost & Compute** | Extremely cheap | Moderate (Vector DB storage) | High (GPU hours required) |
| **Knowledge Recency**| Cutoff date | Real-time live access | Frozen at training date |
| **Hallucination Risk**| Moderate | **Lowest** (Grounded in retrieved sources) | High (Can still hallucinate!) |

---

## 2. Supervised Fine-Tuning (SFT) Data Format

To fine-tune a model, you create a `.jsonl` file where each line is an independent JSON object with conversational turns:

```json
{"messages": [{"role": "system", "content": "You are a Medical Billing Coder."}, {"role": "user", "content": "Patient diagnosed with Type 2 Diabetes without complications."}, {"role": "assistant", "content": "ICD-10-CM Code: E11.9"}]}
{"messages": [{"role": "system", "content": "You are a Medical Billing Coder."}, {"role": "user", "content": "Acute upper respiratory infection, unspecified."}, {"role": "assistant", "content": "ICD-10-CM Code: J06.9"}]}
```

---

## 3. LoRA: Low-Rank Adaptation (How PEFT Saves Millions)

A 70-Billion parameter model has 70,000,000,000 floating point weights.
- **Full Fine-Tuning**: Modifies all 70B weights. You need an entire cluster of 8x A100 GPUs ($80,000+) just to fit the optimizer states in memory!
- **LoRA Breakthrough (2021)**: **Freezes the original base weights ($W_0$)** completely. It injects two tiny low-rank decomposition matrices ($A$ and $B$) beside the attention layers:

$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A)$$

- If rank $r = 8$, you only train **0.05% of the model parameters** (e.g. 35 million instead of 70 billion!).
- The adapter weights can be trained on a single $1,000 consumer GPU and weigh **less than 50 MB** on disk!

```
          ┌────────────────────────────────────────┐
          │   Frozen Pretrained Weights (W_0)      │
          │   (70 Billion Parameters - No change!) │
Input ────┼────────────────────────────────────────┼────► Sum ────► Output
  X       │                                        │       ▲
          │   Matrix A (d x r) ──► Matrix B (r x d)│       │
          │   (Trainable Low-Rank LoRA Adapter)    │───────┘
          └────────────────────────────────────────┘
```

---

## 4. Quantization: Shrinking Models from 140 GB to 4 GB

Weights in deep learning are normally stored as **16-bit floating point numbers (FP16)**:
- 1 parameter in FP16 = 2 Bytes of memory.
- An 8B parameter model requires $8 \times 2 = \mathbf{16\text{ GB}}$ of GPU VRAM just to load!

**Quantization** converts those high-precision floats into low-precision integers (**INT8 or INT4**) with minimal accuracy loss:
- 4-bit Quantization (INT4): 1 parameter = 0.5 Bytes.
- An 8B parameter model shrinks from **16 GB down to 4.5 GB**, allowing it to run smoothly on a standard MacBook or consumer laptop!

### Common Formats:
- **GGUF**: Best for CPU inference using `llama.cpp` or Ollama.
- **AWQ / GPTQ**: Best for high-throughput GPU inference with vLLM.
- **QLoRA**: 4-bit quantized base model with 16-bit LoRA adapters.

---

## 5. Common Fresher Pitfalls

1. **Fine-Tuning to teach an LLM new facts**:
   - ⚠️ **The Classic Mistake**: Fine-tuning is great for learning **format and style**, but terrible for learning **factual knowledge**. Use **RAG** for facts and documentation!
2. **Catastrophic Forgetting during SFT**:
   - Fine-tuning aggressively on only medical codes can cause the model to lose its general conversational ability and reasoning. Mix in general instruction data.
3. **Training on dirty, unvalidated JSONL data**:
   - If your training JSONL contains corrupt formatting or contradictory labels, the fine-tuned model's performance will degrade drastically (**Garbage In, Garbage Out**).

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: Build a LoRA Parameter Calculator & SFT Validator
**Scenario**: You are an MLOps Engineer preparing an open-source model fine-tuning job. Build a tool that validates SFT JSONL datasets and calculates the exact memory and parameter savings of LoRA vs Full Fine-Tuning.

```python
# =========================================================
# Day 25 Lab: LoRA Parameter Calculator & Dataset Validator
# =========================================================
import json

def calculate_lora_efficiency(hidden_dim: int = 4096, rank: int = 8, num_layers: int = 32):
    """Calculates trainable parameters for Query and Value attention projections."""
    # Standard full attention weights per layer (W_q and W_v)
    full_params_per_layer = 2 * (hidden_dim * hidden_dim)
    total_full_params = full_params_per_layer * num_layers

    # LoRA adapters per layer (Matrix A: d x r, Matrix B: r x d)
    lora_params_per_layer = 2 * (hidden_dim * rank + rank * hidden_dim)
    total_lora_params = lora_params_per_layer * num_layers

    reduction_percentage = (1 - (total_lora_params / total_full_params)) * 100
    
    # Memory footprint in FP16 (2 bytes per param)
    full_mem_mb = (total_full_params * 2) / (1024 * 1024)
    lora_mem_mb = (total_lora_params * 2) / (1024 * 1024)

    return {
        "total_full_params": f"{total_full_params:,}",
        "total_lora_params": f"{total_lora_params:,}",
        "parameter_reduction": f"{reduction_percentage:.2f}%",
        "full_weights_size_mb": f"{full_mem_mb:.1f} MB",
        "lora_adapter_size_mb": f"{lora_mem_mb:.2f} MB"
    }

def validate_sft_dataset(sample_records: list[dict]) -> tuple[bool, list[str]]:
    """Validates that conversational turns adhere to the ChatML standard."""
    errors = []
    for idx, row in enumerate(sample_records):
        if "messages" not in row:
            errors.append(f"Row {idx}: Missing 'messages' root key.")
            continue
        roles = [m.get("role") for m in row["messages"]]
        if "user" not in roles or "assistant" not in roles:
            errors.append(f"Row {idx}: Must contain both 'user' and 'assistant' roles.")
    return len(errors) == 0, errors

# Test the Calculator
lora_stats = calculate_lora_efficiency(hidden_dim=4096, rank=8, num_layers=32)

print("="*55)
print("LoRA PEFT EFFICIENCY REPORT")
print("="*55)
for k, v in lora_stats.items():
    print(f"{k:25}: {v}")
print("="*55)

# Test Dataset Validation
dummy_dataset = [
    {"messages": [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]},
    {"corrupt_key": [{"role": "user", "content": "Broken"}]}
]
is_valid, validation_errors = validate_sft_dataset(dummy_dataset)
print(f"\nDataset Valid?: {is_valid} | Detected Issues: {validation_errors}")
```

---

## 7. Interview Quick-Fire Questions

1. **Q: When should you choose RAG over Fine-Tuning?**
   - **Answer**: Choose **RAG** when the model needs access to dynamic, frequently updated, or proprietary factual information (e.g. company documentation, customer databases) with source citations and low hallucination risk. Choose **Fine-Tuning** when you need to adapt the model's style, tone, domain-specific vocabulary, or force adherence to a complex output syntax that prompting struggles to enforce.
2. **Q: How does LoRA (Low-Rank Adaptation) reduce GPU memory consumption during training?**
   - **Answer**: In full fine-tuning, the GPU must store the model weights, gradients, and optimizer states (like Adam's momentum and variance) for all billions of parameters. LoRA freezes the original weights and inserts low-rank matrices with rank $r \ll d$. Because optimizer states are only tracked for the fraction of weights in the adapter, memory requirements drop by over 70%, allowing training on consumer GPUs.
3. **Q: What is the difference between QLoRA and standard LoRA?**
   - **Answer**: Standard LoRA loads the base model in 16-bit floating point and attaches 16-bit adapters. **QLoRA** quantizes the frozen base model down to **4-bit NormalFloat (NF4)** precision, significantly compressing base memory, while backpropagating gradients into 16-bit LoRA adapter matrices, enabling fine-tuning of a 70B model on a single 48GB GPU.
