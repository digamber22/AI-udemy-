# File Structure Notes (Python RAG + FastAPI + RQ)

## 1) Overview

This project follows a clean and modular backend structure. Each folder has a specific responsibility, making the system easy to understand, scale, and maintain.

---

## 2) Project Structure

```bash
rag_queue/
│
├── client/
│   ├── __init__.py
│   ├── rq_client.py
│
├── queues/
│   ├── __init__.py
│   ├── worker.py
│
├── docker-compose.yml
├── main.py
├── server.py
```

---

## 3) What is `__init__.py`

### Definition

`__init__.py` is a special Python file that tells Python:

> This folder should be treated as a package.

---

### Why it is used

* Allows importing modules from that folder
* Helps organize code into packages
* Makes folder structure work like a Python module system

---

### Example

Without `__init__.py`, imports may fail.

With it, you can do:

```python
from rag_queue.client.rq_client import queue
from rag_queue.queues.worker import process_query
```

---

### Optional Uses

You can also use `__init__.py` to:

#### 1. Simplify imports

```python
# client/__init__.py
from .rq_client import queue
```

Then:

```python
from rag_queue.client import queue
```

#### 2. Run initialization code (rare)

```python
print("Client package loaded")
```

---

### Important Note

* In Python 3.3+, it is optional
* But in real-world projects → always include it (best practice)

---

## 4) Folder-wise Explanation

### 📁 `rag_queue/` (Root Folder)

* Main project package
* Used when running the app as a module

Run command:

```bash
python -m rag_queue.main
```

---

### 📁 `client/` (Queue / External Services Layer)

Files:

* `rq_client.py`

Purpose:

* Manages Redis connection
* Creates and manages RQ queue

Why important:

* Keeps external service logic separate
* Improves maintainability

---

### 📁 `queues/` (Worker Layer)

Files:

* `worker.py`

Purpose:

* Contains background job logic
* Processes queued tasks

In this project:

* Runs RAG pipeline
* Performs vector search
* Calls OpenAI

---

### 📄 `server.py` (API Layer)

Purpose:

* Handles HTTP requests
* Sends jobs to queue
* Returns job IDs and results

Endpoints:

* `/chat` → enqueue query
* `/job-status` → get result

---

### 📄 `main.py` (Application Entry Point)

Purpose:

* Starts FastAPI application
* Used with module execution

```bash
python -m rag_queue.main
```

---

### 🐳 `docker-compose.yml` (Infrastructure Layer)

Purpose:

* Runs required services
* Example:

  * Qdrant (vector database)
  * Redis (queue system)

---

## 5) Full System Flow

```text
User → FastAPI (server.py)
        ↓
     RQ Queue (client/)
        ↓
     Worker (queues/)
        ↓
     Qdrant + OpenAI
        ↓
     Result stored
        ↓
User fetches result (/job-status)
```

---

## 6) Why this Structure is Good

* Clear separation of concerns
* Easy to scale (add more workers or services)
* Easy to debug
* Industry-standard backend design

---

## 7) One-line Summary

* `__init__.py` → makes folders Python packages
* Structure → separates API, queue, worker, and infrastructure cleanly
