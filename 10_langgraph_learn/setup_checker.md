# LangGraph + MongoDB Checkpoint Setup (Complete Guide)

This guide explains how to set up **LangGraph with MongoDB checkpointing** so your agent can remember previous conversations using the same `thread_id`.

---

## 🧠 Concept (Quick Understanding)

- **Checkpoint** → saved state after each step  
- **MongoDB** → stores the state  
- **thread_id** → identifies conversation  
- Same thread → memory works  
- No checkpoint → agent forgets everything  

### Example
- Input: `My name is Digamber`  
- Next: `What is my name?`  
- ✅ With checkpoint → "Digamber"  
- ❌ Without checkpoint → No memory  

---

## 🚀 Setup (All Steps in One Flow)

```bash
# 1) Create project folder and enter it
mkdir langgraph-checkpoint-demo && cd langgraph-checkpoint-demo

# 2) Create virtual environment
python -m venv .venv

# 3) Activate virtual environment
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux / macOS
# source .venv/bin/activate

# 4) Install dependencies
python -m pip install --upgrade pip
pip install langgraph langchain langchain-openai langgraph-checkpoint-mongodb pymongo python-dotenv

# 5) Create .env file (manually)
# OPENAI_API_KEY=your_openai_api_key_here

# 6) Create docker-compose.yml (manually)

version: "3.8"

services:
  mongodb:
    image: mongo:7
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin
    restart: always

# 7) Start MongoDB container
docker compose up -d

# 8) Verify MongoDB is running
docker ps

# 9) Run your LangGraph app
python app.py