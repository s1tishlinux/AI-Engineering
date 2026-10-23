# Day 13: REST API Integration & Modern HTTP Clients

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The architecture of RESTful APIs: Client-Server, Statelessness, and HTTP Request/Response cycles.
2. Standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`) and HTTP Status Codes.
3. Consuming third-party APIs using Python's modern async HTTP client: **`httpx`** (and `requests`).
4. Passing Authentication headers (Bearer Tokens, API Keys), query parameters, and JSON payloads.
5. Production-grade resilience: handling timeouts, pagination, rate limits (`429 Too Many Requests`), and Exponential Backoff.

---

## 1. The "Why": APIs are the Glue of Modern AI

You don't host Gemini, Claude, or Stripe on your local laptop. They live on massive cloud clusters across the globe.
Your Python applications communicate with these models and services using **HTTP REST APIs**.
If your API integration code crashes when the network hiccups or misses pagination, your AI pipeline will fail in production.

---

## 2. HTTP Fundamentals & Status Codes

Every HTTP transaction contains:
- **Request**: URL, Method (Verb), Headers (Auth, Content-Type), and Body (JSON).
- **Response**: Status Code, Headers, and Body (JSON/Text).

### Status Codes You Must Know for Interviews:
| Status Code Category | Meaning | Key Examples |
| :--- | :--- | :--- |
| **2xx (Success)** | Request completed successfully | `200 OK` (Fetched), `201 Created` (Saved resource) |
| **3xx (Redirection)** | Resource moved | `301 Moved Permanently`, `304 Not Modified` |
| **4xx (Client Error)** | You made a mistake | `400 Bad Request`, `401 Unauthorized` (Missing token), `403 Forbidden`, `404 Not Found`, `429 Too Many Requests` (Rate limit) |
| **5xx (Server Error)** | The remote server crashed | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable` |

---

## 3. Modern Async HTTP: Why `httpx` Beats `requests`

`requests` is synchronous and blocks the event loop. **`httpx`** provides identical syntax to `requests` while offering full native **async/await support** and HTTP/2 capabilities.

```python
import httpx
import asyncio

# Asynchronous GET request
async def fetch_github_user(username: str):
    url = f"https://api.github.com/users/{username}"
    headers = {"User-Agent": "TeachIn-Python-Client"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers=headers)
        
        # Check HTTP Status Code
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User: {data['name']} | Public Repos: {data['public_repos']}")
        elif response.status_code == 404:
            print(f"❌ User '{username}' does not exist on GitHub.")
        else:
            print(f"⚠️ Unexpected Status: {response.status_code}")

asyncio.run(fetch_github_user("torvalds"))
```

---

## 4. POST Requests with Authentication & JSON Payloads

```python
import httpx
import asyncio

# Simulating an API call to an LLM provider endpoint
async def call_ai_generation_api(prompt: str, api_token: str):
    endpoint = "https://api.example-ai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 256
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Notice how we pass json=payload (automatically serializes to JSON string)
            response = await client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raises HTTPStatusError if 4xx or 5xx!
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"🚨 API Error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"🌐 Network / DNS Failure: {e}")
```

---

## 5. Production Resilience: Handling Rate Limits (`429`) & Retries

AI APIs (especially OpenAI and Anthropic) have strict Tokens-Per-Minute (TPM) and Requests-Per-Minute (RPM) quotas. When exceeded, they return `429 Too Many Requests`.

### The Strategy: Exponential Backoff with Jitter
Instead of hammering the server, wait: $2^0 = 1s$, $2^1 = 2s$, $2^2 = 4s$, plus small random jitter.

```python
import asyncio
import random
import httpx

async def resilient_api_fetch(url: str, max_retries: int = 3):
    async with httpx.AsyncClient() as client:
        for attempt in range(1, max_retries + 1):
            try:
                response = await client.get(url, timeout=5.0)
                
                # Check for rate limit
                if response.status_code == 429:
                    wait_time = (2 ** attempt) + random.uniform(0.1, 0.5)
                    print(f"⚠️ [429 RATE LIMIT] Backing off for {wait_time:.2f}s (Attempt {attempt}/{max_retries})...")
                    await asyncio.sleep(wait_time)
                    continue

                response.raise_for_status()
                return response.json()

            except (httpx.TimeoutException, httpx.NetworkError) as err:
                print(f"⚠️ Network glitch on attempt {attempt}: {err}")
                await asyncio.sleep(1.0)

    raise ConnectionError("Exhausted all retries. API remains unavailable.")
```

---

## 6. Common Fresher Pitfalls

1. **Creating a new `httpx.AsyncClient()` on every single request**:
   - Creating a client opens a new TCP connection pool and SSL handshake every time. Reuse a single shared client instance using `async with httpx.AsyncClient() as client:` across multiple calls!
2. **Not configuring timeouts**:
   - By default, many HTTP requests wait forever if a remote server hangs. Always set an explicit `timeout=10.0`.
3. **Assuming `response.json()` always succeeds**:
   - If a server crashes and returns raw HTML (`502 Bad Gateway`), calling `response.json()` raises `json.JSONDecodeError`. Always check `response.status_code == 200` first or use `response.raise_for_status()`.

---

## 7. Daily Hands-On Lab

### 🧪 Exercise: Build a Multi-Page Weather & Pollution Aggregator
**Scenario**: Consume the public Open-Meteo REST API to fetch temperature, wind speed, and weather codes for multiple tech hubs (Hyderabad, Bengaluru, San Francisco) concurrently without blocking.

```python
# =========================================================
# Day 13 Lab: Concurrent City Weather Aggregator
# =========================================================
import asyncio
import httpx

CITIES = [
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    {"name": "Bengaluru", "lat": 12.9716, "lon": 77.5946},
    {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194}
]

async def fetch_city_weather(client: httpx.AsyncClient, city: dict) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto"
    }

    try:
        resp = await client.get(url, params=params, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()["current"]
        return {
            "city": city["name"],
            "temperature_c": data["temperature_2m"],
            "wind_speed_kmh": data["wind_speed_10m"],
            "status": "SUCCESS"
        }
    except Exception as e:
        return {"city": city["name"], "error": str(e), "status": "FAILED"}

async def main():
    print("🌍 Fetching weather metrics for global tech hubs concurrently...\n")
    async with httpx.AsyncClient() as shared_client:
        tasks = [fetch_city_weather(shared_client, c) for c in CITIES]
        results = await asyncio.gather(*tasks)

    print("="*50)
    print("WEATHER REPORT SUMMARY")
    print("="*50)
    for r in results:
        if r["status"] == "SUCCESS":
            print(f"📍 {r['city']:15}: {r['temperature_c']}°C (Wind: {r['wind_speed_kmh']} km/h)")
        else:
            print(f"📍 {r['city']:15}: Error ({r['error']})")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 8. Interview Quick-Fire Questions

1. **Q: What is the difference between `PUT` and `POST` in RESTful API design?**
   - **Answer**: `POST` is typically used to create a new resource on the server and is **not idempotent** (calling it 5 times creates 5 distinct resources). `PUT` is used to update or replace an existing resource and is **idempotent** (calling it 5 times with the exact same payload results in the exact same server state).
2. **Q: What is the difference between `401 Unauthorized` and `403 Forbidden`?**
   - **Answer**: `401 Unauthorized` means **authentication is missing or invalid** ("We don't know who you are; please provide a valid token"). `403 Forbidden` means **authentication succeeded, but authorization is denied** ("We know who you are, but you do not have permission to access this resource").
3. **Q: Why is connection pooling in `httpx.AsyncClient` important?**
   - **Answer**: Establishing an HTTPS connection requires a multi-step TCP handshake and SSL/TLS certificate negotiation, which can take 100–300 ms. Reusing an `AsyncClient` keeps existing TCP sockets alive and pools connections, drastically lowering latency across multiple API calls.
