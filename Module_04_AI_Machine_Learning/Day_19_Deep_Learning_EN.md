# Day 19: Deep Learning Fundamentals (Neural Networks & PyTorch)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The biological inspiration: Biological Neurons vs **Artificial Perceptrons**.
2. Network architecture: Input Layer, Hidden Layers, Output Layer, Weights ($W$), and Biases ($b$).
3. Why non-linearity is mandatory: **Activation Functions** (ReLU, Sigmoid, Softmax).
4. The learning engine: **Forward Pass**, **Loss Functions**, **Backpropagation (Chain Rule)**, and **Gradient Descent**.
5. The PyTorch ecosystem: Tensors, GPU acceleration (`cuda`), Autograd, and `torch.nn.Module`.
6. Early NLP foundations: Bag of Words, TF-IDF, and Word Embeddings.

---

## 1. The "Why": Why Deep Learning Replaced Traditional ML

Traditional Machine Learning (Days 16–18) requires **manual feature engineering**:
- To detect a cat in an image, a human engineer had to manually calculate edge detectors, color histograms, and texture ratios.
- If lighting changed, the manual rules broke!

**Deep Learning discovers features automatically**:
- Layer 1 learns simple edges and lines.
- Layer 2 combines edges into curves and textures.
- Layer 3 combines curves into noses, ears, and whiskers.
- Output Layer recognizes the cat!

---

## 2. Anatomy of an Artificial Neuron (The Perceptron)

A single artificial neuron takes inputs $X_1, X_2, \dots, X_n$, multiplies them by trainable weights $W$, adds a bias $b$, and passes the sum through an activation function:

$$z = \sum (X_i \cdot W_i) + b = W^T X + b$$
$$\text{Output} = f(z)$$

```
Inputs (X)       Weights (W)        Summation & Bias        Activation (f)      Output (y)
  X1 ─────────────► W1 ────────┐
                               │
  X2 ─────────────► W2 ────────┼───► [ z = Σ(X·W) + b ] ───► [ f(z) = ReLU ] ────► Prediction
                               │
  X3 ─────────────► W3 ────────┘
```

---

## 3. Activation Functions: Why Do We Need Them?

Without activation functions, stacking 100 linear layers is mathematically equivalent to just **one single linear regression layer**!
Activation functions introduce **non-linearity**, allowing neural networks to approximate any complex curve in the universe (Universal Approximation Theorem).

| Activation | Mathematical Formula | Range | Best Used For |
| :--- | :--- | :--- | :--- |
| **ReLU (Rectified Linear Unit)** | $f(z) = \max(0, z)$ | $[0, \infty)$ | **Default choice for all hidden layers** (Solves vanishing gradient!) |
| **Sigmoid** | $\sigma(z) = \frac{1}{1 + e^{-z}}$ | $(0, 1)$ | Output layer for **Binary Classification** |
| **Softmax** | $\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum e^{z_j}}$ | $(0, 1)$ (Sum to 1.0) | Output layer for **Multi-Class Classification** |

---

## 4. How Neural Networks Learn: Backpropagation & Gradient Descent

Learning in neural networks is an iterative 4-step loop:

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  1. FORWARD     │ ───►  │  2. COMPUTE     │ ───►  │  3. BACKPROP    │ ───►  │  4. UPDATE      │
│  PASS           │       │  LOSS           │       │  (Chain Rule)   │       │  WEIGHTS        │
│  Generate y_hat │       │  Error = y - y^ │       │  Calculate dL/dW│       │  W = W - α(dL/dW│
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
         ▲                                                                             │
         └──────────────────────────── Repeat for N Epochs ────────────────────────────┘
```

- **Loss Function**: Measures how wrong the model is (e.g. Cross-Entropy Loss).
- **Backpropagation**: Uses calculus (the chain rule) to calculate how much each individual weight contributed to the total error ($\frac{\partial \text{Loss}}{\partial W}$).
- **Gradient Descent**: Updates each weight in the opposite direction of the slope, scaled by the **Learning Rate ($\alpha$)**:
  $$W_{\text{new}} = W_{\text{old}} - \alpha \cdot \frac{\partial \text{Loss}}{\partial W}$$

---

## 5. PyTorch in Action: Building a Neural Network

PyTorch is the undisputed king of modern AI research and LLM development.

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Define a Multi-Layer Perceptron (MLP)
class SimpleClassifier(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        super().__init__()
        # Layer 1: Input to Hidden
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        # Non-linear activation
        self.relu = nn.ReLU()
        # Layer 2: Hidden to Output
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# Simulated Toy Dataset (4 samples, 3 input features)
X_train = torch.tensor([[1.0, 2.0, 0.5], [2.0, 1.0, 0.8], [0.5, 0.2, 0.1], [3.0, 2.5, 1.2]])
y_train = torch.tensor([1, 1, 0, 1])  # Binary targets

# Instantiate Model, Loss Function, and Optimizer
model = SimpleClassifier(input_dim=3, hidden_dim=8, output_dim=2)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training Loop (50 Epochs)
print("Training Neural Network...")
for epoch in range(1, 51):
    optimizer.zero_grad()               # 1. Clear old gradients
    predictions = model(X_train)        # 2. Forward pass
    loss = criterion(predictions, y_train) # 3. Compute loss
    loss.backward()                     # 4. Backward pass (Backprop)
    optimizer.step()                    # 5. Update weights

    if epoch % 10 == 0:
        print(f"Epoch [{epoch:02d}/50] - Loss: {loss.item():.4f}")

# Inference on a new sample
sample = torch.tensor([[0.2, 0.1, 0.05]])
with torch.no_grad():
    raw_logits = model(sample)
    predicted_class = torch.argmax(raw_logits, dim=1).item()
    print(f"\nInference Result for sample: Class {predicted_class}")
```

---

## 6. Common Fresher Pitfalls

1. **Forgetting `optimizer.zero_grad()`**:
   - In PyTorch, gradients accumulate by default! If you omit `zero_grad()`, gradients from the previous epoch add up to the current epoch, causing your weights to explode.
2. **Learning Rate ($\alpha$) Pitfalls**:
   - Too high ($\alpha = 1.0$): Loss diverges and oscillates to infinity (`NaN`).
   - Too low ($\alpha = 0.0000001$): Model takes weeks to converge.
3. **Evaluating without `torch.no_grad()`**:
   - Running inference without `torch.no_grad()` keeps building the computation graph in memory, rapidly consuming all GPU VRAM.

---

## 7. Daily Hands-On Lab

### 🧪 Exercise: Build a PyTorch Binary Sentiment Classifier
**Scenario**: Classify customer review embeddings (dimension = 4) into Positive (1) or Negative (0) using a PyTorch neural network.

```python
# =========================================================
# Day 19 Lab: PyTorch Sentiment Classification Network
# =========================================================
import torch
import torch.nn as nn
import torch.optim as optim

# Simulated 4-dimensional word embeddings for reviews
# [pos_words, neg_words, length_ratio, exclamation_intensity]
X_reviews = torch.tensor([
    [0.9, 0.1, 0.5, 0.8],  # "Fantastic customer service! Absolutely loved it!" -> 1
    [0.8, 0.2, 0.3, 0.6],  # "Great product, fast delivery."                   -> 1
    [0.1, 0.9, 0.8, 0.9],  # "Terrible experience, broken on arrival!"        -> 0
    [0.2, 0.8, 0.4, 0.3]   # "Waste of money, poor quality."                  -> 0
], dtype=torch.float32)

y_sentiment = torch.tensor([[1.0], [1.0], [0.0], [0.0]], dtype=torch.float32)

class SentimentNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()  # Outputs probability between 0.0 and 1.0
        )

    def forward(self, x):
        return self.network(x)

net = SentimentNetwork()
criterion = nn.BCELoss()  # Binary Cross Entropy Loss
optimizer = optim.SGD(net.parameters(), lr=0.1)

# Train the network
for epoch in range(1, 101):
    optimizer.zero_grad()
    outputs = net(X_reviews)
    loss = criterion(outputs, y_sentiment)
    loss.backward()
    optimizer.step()

# Test on a new review embedding
new_review = torch.tensor([[0.85, 0.15, 0.4, 0.7]])
with torch.no_grad():
    prob = net(new_review).item()
    print("="*45)
    print("SENTIMENT INFERENCE")
    print("="*45)
    print(f"Positive Sentiment Probability: {prob * 100:.2f}%")
    print(f"Final Classification: {'POSITIVE' if prob >= 0.5 else 'NEGATIVE'}")
    print("="*45)
```

---

## 8. Interview Quick-Fire Questions

1. **Q: Why is ReLU preferred over Sigmoid in the hidden layers of deep neural networks?**
   - **Answer**: The Sigmoid function saturates at extreme values ($z > 4$ or $z < -4$), causing its derivative to become nearly zero. When multiplying these small gradients across many layers during backpropagation, gradients vanish to zero (**Vanishing Gradient Problem**), preventing early layers from learning. ReLU has a constant derivative of 1 for all positive inputs, allowing deep networks to train effectively.
2. **Q: What is the difference between Batch, Mini-Batch, and Stochastic Gradient Descent (SGD)?**
   - **Answer**: **Batch GD** computes loss over the entire dataset before making one weight update (slow, high memory). **Pure SGD** updates weights after every single training sample (fast, but noisy). **Mini-Batch GD** (the modern standard, typically batch sizes of 32, 64, or 128) strikes the optimal balance between computational efficiency and gradient stability.
3. **Q: What is the purpose of the Softmax function?**
   - **Answer**: Softmax normalizes a vector of raw unconstrained model outputs (logits) into a valid probability distribution over $K$ classes, where each probability is strictly between 0 and 1 and the sum of all probabilities equals exactly 1.0.
