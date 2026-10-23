# Day 10: Data Structures, Generators & Algorithms (Module 02 Capstone)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Core Linear Data Structures: **Stacks** (LIFO) and **Queues** (FIFO using `collections.deque`).
2. The Python Iterator Protocol: `__iter__()` and `__next__()`.
3. **Generators and `yield`**: The secret to streaming gigabytes of data without running out of RAM (Lazy Evaluation).
4. Big-O Complexity: Intuitive understanding of $O(1)$, $O(\log n)$, $O(n)$, and $O(n \log n)$.
5. Fundamental Searching (Binary Search) and Python's built-in **Timsort**.
6. **Module 02 Capstone Mini-Project**: High-Throughput Log Stream Engine using custom generators and queues.

---

## 1. The "Why": Scalability & Big Data in AI

Imagine loading a 10 GB file of documents into Python to generate vector embeddings.
- If you do `file.readlines()`, Python tries to load all 10 GB directly into your RAM. On a standard 8GB or 16GB laptop, **the OS crashes immediately with an `Out of Memory (OOM)` error**.
- If you use a **Generator (`yield`)**, Python loads **only 1 line at a time** into RAM, processes it, and discards it. Total memory consumed? **Less than 50 KB!**

---

## 2. Linear Data Structures: Stacks & Queues

### A. Stack (LIFO: Last In, First Out)
- **Analogy**: A stack of cafeteria plates. The plate you place on top last is the first one someone picks up.
- **Use Case in Tech**: Undo/Redo operations, browser back button, function call stacks.

```python
# A standard Python list acts as a perfect Stack using .append() and .pop()
browser_history = []

# Navigating pages (Push)
browser_history.append("google.com")
browser_history.append("github.com")
browser_history.append("openai.com")

# Pressing the 'Back' button (Pop)
current_page = browser_history.pop()
print("Popped (Navigated back from):", current_page)  # openai.com
print("Current page is now:", browser_history[-1])   # github.com
```

### B. Queue (FIFO: First In, First Out)
- **Analogy**: A queue of passengers waiting at a ticket counter. The first person to arrive is the first person served.
- **Use Case in Tech**: Background task workers, message queues (RabbitMQ, Kafka, AWS SQS).
- ⚠️ **Fresher Rule**: **NEVER use `list.pop(0)` for a queue!** Popping from the beginning of a list forces Python to shift all $N$ remaining elements in memory, causing a terrible $O(n)$ performance penalty. Always use `collections.deque` for $O(1)$ popleft!

```python
from collections import deque

# High-performance double-ended queue
request_queue = deque()

# Adding incoming customer tickets
request_queue.append("Ticket #101: Reset Password")
request_queue.append("Ticket #102: Refund Request")
request_queue.append("Ticket #103: API Latency Alert")

# Worker processing tickets in FIFO order (O(1) time complexity)
served_ticket = request_queue.popleft()
print(f"Processed: {served_ticket}")  # Ticket #101
print(f"Next in line: {request_queue[0]}")
```

---

## 3. Iterators and Generators (`yield`)

### A. The Iterator Protocol
Any object that can be looped over implements `__iter__()`. Calling `next()` on it retrieves the subsequent item until it raises `StopIteration`.

### B. Generators: Functions that `yield`
When a function uses `yield` instead of `return`, it pauses execution and produces a value. When called again, it resumes **right from where it left off**!

```python
# A Generator that produces an infinite or massive sequence lazily
def stream_sensor_readings(limit: int):
    val = 1
    while val <= limit:
        # yield pauses execution and sends value to caller without destroying state!
        yield f"Telemetry Sensor Ping #{val} | Temp: {20 + val * 0.5}°C"
        val += 1

# Creating generator object (costs almost zero RAM)
sensor_stream = stream_sensor_readings(1000000)
print("Type:", type(sensor_stream))

# Pulling items on demand (Lazy Evaluation)
print(next(sensor_stream))
print(next(sensor_stream))
```

---

## 4. Big-O Complexity Made Simple

Big-O describes how the runtime of your algorithm scales as the dataset $N$ grows from 10 to 10,000,000 items:

| Big-O Notation | Name | Practical Example | Scaling Speed |
| :--- | :--- | :--- | :--- |
| **$O(1)$** | Constant | Looking up a key in a Dictionary or Set | Instant (0.001 ms) |
| **$O(\log n)$** | Logarithmic | Binary Search in a sorted array | Extremely Fast |
| **$O(n)$** | Linear | Looping over an unsorted list with `for item in list` | Fair / Proportional |
| **$O(n \log n)$** | Linearithmic | Python's built-in `list.sort()` (Timsort) | Standard for Sorting |
| **$O(n^2)$** | Quadratic | Nested loops (`for i in ...: for j in ...:`) | Slow (Crashes on big data) |

---

## 5. Searching Algorithms: Linear vs Binary Search

### Binary Search ($O(\log n)$): Divide and Conquer
If a dataset is sorted, you don't need to check all 1,000,000 elements. You check the middle element. If your target is smaller, discard the entire right half!

```python
def binary_search(sorted_list: list[int], target: int) -> int:
    """Returns index of target if found, else -1. Runs in O(log n)."""
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = sorted_list[mid]

        if mid_val == target:
            return mid  # Found target
        elif mid_val < target:
            low = mid + 1  # Discard left half
        else:
            high = mid - 1  # Discard right half

    return -1

# Searching in 1 million numbers
large_sorted_data = list(range(0, 1000000, 2))  # [0, 2, 4, ... 999998]
target_num = 754320

index = binary_search(large_sorted_data, target_num)
print(f"Target {target_num} found at index: {index}")  # Took only ~20 checks out of 1 million!
```

---

## 6. Common Fresher Pitfalls

1. **Converting generators to lists unnecessarily**:
   - Writing `list(my_generator)` immediately defeats the entire purpose of a generator by forcing all million records into RAM at once!
2. **Re-running an exhausted generator**:
   - A generator can only be consumed **once**. After reaching the end, calling `next()` raises `StopIteration`. You must instantiate a new generator object to loop again.
3. **Using nested loops ($O(n^2)$) to check intersections**:
   - Converting one list to a `set` drops membership checks from $O(n^2)$ to $O(n)$.

---

## 7. Module 02 Capstone Project: Streaming Log Engine

This capstone combines OOP classes, Queues (`deque`), Generators (`yield`), and Big-O efficiency into a simulated real-time log ingestion and search system.

```python
# =================================================================
# Module 02 Capstone: High-Throughput Log Streaming & Search Engine
# =================================================================
from collections import deque
from typing import Generator
import time

class LogRecord:
    def __init__(self, log_id: int, level: str, message: str):
        self.log_id = log_id
        self.level = level
        self.message = message

    def __repr__(self):
        return f"[{self.level}] #{self.log_id:04d}: {self.message}"

class LogStreamSimulator:
    """Simulates a high-volume live server log producer using Generators."""
    @staticmethod
    def generate_logs(count: int) -> Generator[LogRecord, None, None]:
        levels = ["INFO", "DEBUG", "INFO", "WARNING", "ERROR"]
        messages = [
            "User login successful",
            "Cache miss, fetching from Redis",
            "Database connection established",
            "High CPU temperature detected",
            "Payment Gateway connection timeout"
        ]
        for i in range(1, count + 1):
            lvl = levels[i % len(levels)]
            msg = messages[i % len(messages)]
            # Yield lazily produces records without hoarding memory
            yield LogRecord(log_id=i, level=lvl, message=msg)

class RealtimeLogMonitor:
    def __init__(self, buffer_size: int = 5):
        # A sliding window queue keeping only the most recent N logs in memory
        self.sliding_buffer = deque(maxlen=buffer_size)
        self.error_count = 0

    def ingest_stream(self, log_generator: Generator[LogRecord, None, None]):
        print(f"📡 Starting Real-Time Ingestion (Sliding Window: {self.sliding_buffer.maxlen})...\n")
        for log in log_generator:
            self.sliding_buffer.append(log)
            if log.level == "ERROR":
                self.error_count += 1
                print(f"🚨 CRITICAL ALERT: {log}")

    def display_latest_state(self):
        print("\n" + "="*50)
        print("📊 RECENT SYSTEM LOG BUFFER (SLIDING WINDOW)")
        print("="*50)
        for log in self.sliding_buffer:
            print("  ", log)
        print(f"\nTotal Critical Errors Ingested: {self.error_count}")
        print("="*50)

# Run the Capstone
if __name__ == "__main__":
    stream = LogStreamSimulator.generate_logs(count=25)
    monitor = RealtimeLogMonitor(buffer_size=5)
    monitor.ingest_stream(stream)
    monitor.display_latest_state()
```

---

## 8. Interview Quick-Fire Questions

1. **Q: What is the difference between `return` and `yield` in Python?**
   - **Answer**: `return` exits the function, passes a single final value back to the caller, and destroys the function's local execution stack. `yield` pauses the function, emits a value to the caller, and preserves its internal execution state and local variables so it can resume right after the `yield` statement on the next call.
2. **Q: Why is `collections.deque` preferred over `list` for implementing a FIFO queue?**
   - **Answer**: Python lists are dynamic contiguous memory arrays. Removing the first item (`list.pop(0)`) requires shifting all subsequent $N$ elements in memory, which takes $O(n)$ time. `collections.deque` is implemented as a doubly linked list of blocks, providing guaranteed $O(1)$ time complexity for both append and pop operations on either end.
3. **Q: What is the average time complexity of searching for an element in a Python list vs a set?**
   - **Answer**: Searching a Python list takes $O(n)$ linear time because Python must inspect each element one by one. Searching a set takes $O(1)$ constant time on average because sets use hash tables with direct hash-based bucket indexing.
