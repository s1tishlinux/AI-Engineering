# Day 08: Modules, Packages & Virtual Environments

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The difference between a **Script**, a **Module** (`.py`), and a **Package** (folder with `__init__.py`).
2. How Python imports work: `sys.path`, absolute vs relative imports, and circular import traps.
3. The sacred entrypoint condition: `if __name__ == "__main__":`.
4. Creating isolated environments with `venv` (why global `pip install` is catastrophic).
5. Managing dependencies cleanly using `requirements.txt`.

---

## 1. The "Why": Preventing Dependency Hell

Imagine you have two projects on your laptop:
- **Project A (Legacy 2024)** requires `langchain==0.1.0`.
- **Project B (Modern 2026)** requires `langchain==0.3.5`.

If you install packages globally on your machine, installing Project B **overwrites and breaks** Project A!
**Virtual Environments** create private, isolated sandbox folders for each project, ensuring clean reproducible builds.

---

## 2. Modules vs Packages Explained

- **Module**: Any single Python file containing variables, classes, and functions (e.g. `data_cleaner.py`).
- **Package**: A folder containing multiple modules plus an `__init__.py` file (which tells Python: *"Treat this directory as an importable package"*).

### Standard Project Architecture:
```text
my_ai_app/
│
├── .venv/                   # Isolated virtual environment (DO NOT COMMIT TO GIT!)
├── requirements.txt         # Pinned project dependencies
├── main.py                  # Application entry point
│
└── core/                    # Package
    ├── __init__.py          # Package initializer
    ├── model_loader.py      # Module
    └── token_counter.py     # Module
```

---

## 3. The Sacred `if __name__ == "__main__":`

When Python executes a file directly from the terminal (`python main.py`), it automatically sets a hidden internal variable:
`__name__ = "__main__"`

However, if another file imports that module (`import main`), Python sets:
`__name__ = "main"`

```python
# math_utils.py

def add(a, b):
    return a + b

# This block executes ONLY when you run 'python math_utils.py' directly.
# It will NEVER execute when another file does 'import math_utils'!
if __name__ == "__main__":
    print("Testing math_utils locally...")
    assert add(2, 3) == 5
    print("All unit tests passed!")
```

---

## 4. Virtual Environments (`venv`) Workflow

### Step 1: Create a Virtual Environment
Run in your project root:
```bash
# macOS / Linux
python3 -m venv .venv

# Windows
python -m venv .venv
```

### Step 2: Activate the Environment
```bash
# macOS / Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```
*(Notice your terminal prompt will now show `(.venv)` in front!)*

### Step 3: Install & Freeze Dependencies
```bash
# Install required libraries inside the sandbox
pip install pydantic httpx python-dotenv

# Export exact versions to requirements.txt
pip freeze > requirements.txt
```

### Step 4: Deactivate when done
```bash
deactivate
```

---

## 5. Absolute vs Relative Imports

```python
# Inside core/token_counter.py

# 1. Absolute Import (Recommended in modern Python)
from core.model_loader import get_active_model

# 2. Relative Import (Dots represent parent/current directory)
from .model_loader import get_active_model  # Same directory
from ..config import APP_VERSION           # One directory up
```

---

## 6. Common Fresher Pitfalls

1. **Naming your script after a standard library**:
   - ⚠️ **The Classic Disaster**: If you name your file `math.py`, `random.py`, or `json.py`, typing `import math` will import **your file** instead of Python's built-in module, resulting in `AttributeError` everywhere!
2. **Committing `.venv` or `__pycache__` to GitHub**:
   - Always add `.venv/` and `__pycache__/` to your `.gitignore` file. Only commit `requirements.txt`.
3. **Circular Imports**:
   - File A imports File B, while File B imports File A. This causes `ImportError: cannot import name ... from partially initialized module`. Break circular dependencies by extracting common logic into a third file (`common.py`).

---

## 7. Daily Hands-On Lab

### 🧪 Exercise: Build a Modular AI Configuration Package
**Scenario**: You are structuring a production-grade AI repository. Build a standalone package with configuration loaders, environment variable checks, and safety masks.

```python
# ==========================================
# Day 8 Lab: Modular Config & Secret Manager
# ==========================================
import os
import sys

# Simulated configuration module (normally in config/settings.py)
class AppConfig:
    def __init__(self):
        # Reads from environment or falls back to defaults
        self.app_env = os.getenv("APP_ENV", "development")
        self.api_key = os.getenv("GEMINI_API_KEY", "dummy-default-key-xyz123")
        self.debug_mode = self.app_env == "development"

    def get_masked_key(self) -> str:
        """Returns API key with secrets hidden."""
        if len(self.api_key) <= 6:
            return "******"
        return f"{self.api_key[:4]}...{self.api_key[-3:]}"

    def display_environment(self):
        print("="*45)
        print(f"🚀 RUNTIME ENVIRONMENT : {self.app_env.upper()}")
        print(f"🛠️ DEBUG MODE ACTIVE   : {self.debug_mode}")
        print(f"🔑 ACTIVE API KEY      : {self.get_masked_key()}")
        print(f"🐍 PYTHON EXECUTABLE   : {sys.executable}")
        print("="*45)

if __name__ == "__main__":
    print("Validating configuration module directly...")
    config = AppConfig()
    config.display_environment()
```

---

## 8. Interview Quick-Fire Questions

1. **Q: What is the purpose of `__init__.py` in a directory?**
   - **Answer**: Historically in Python 2 and early Python 3, `__init__.py` was required for Python to recognize a directory as a regular package. In Python 3.3+ (PEP 420), implicit namespace packages are supported without it, but `__init__.py` remains best practice to control package exports (`__all__`), expose public APIs, and run package-level initialization code.
2. **Q: What does `sys.path` contain?**
   - **Answer**: `sys.path` is a list of directory paths where the Python interpreter looks for modules when an `import` statement is executed. It starts with the directory of the running script, followed by the standard library directories and site-packages (installed virtual environment packages).
3. **Q: Why should you never commit the virtual environment folder (`.venv`) to Git?**
   - **Answer**: Virtual environments are OS-specific, architecture-dependent (e.g. macOS ARM64 vs Windows x86), and can contain thousands of binary files. Instead, you commit only `requirements.txt` or `pyproject.toml`, allowing team members to recreate the exact environment on their machine using `pip install -r requirements.txt`.
