# Local LLMs Deployment and API Integration

This guide explains how to run local large language models (LLMs) using Docker, Ollama, and Open WebUI.

The goal is to create a private AI environment where you can:
- Run models locally
- Test them safely
- Interact via web UI or API

---

## 1. Install Docker

Download and install Docker from the official website.

### Verify Installation

```bash
docker --version
```

### Test Docker

```bash
docker pull busybox
docker run busybox ls
docker container ps -a
docker container rm <container_id>
```

### Meaning

- `docker pull busybox` → Downloads a small image  
- `docker run busybox ls` → Runs container and executes command  
- `docker container ps -a` → Lists all containers  
- `docker container rm` → Deletes container  

### Notes

- Docker must be **running in background** before using commands  
- If commands fail, restart Docker Desktop  
- Use `docker images` to see downloaded images  
- Containers are temporary unless volumes are used  

---

## 2. Run Ollama in Docker

Ollama allows you to run LLMs locally.

### Test Ollama

```bash
docker run ollama/ollama
```

### Run in Background

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Meaning

- `-d` → Runs in background  
- `-v` → Stores model files permanently  
- `-p` → Exposes API port  
- `--name` → Container name  

### Access

http://localhost:11434

### Notes

- First run may take time (image download)  
- Models are stored inside Docker volume (`ollama`)  
- If port `11434` is busy, change it like `-p 11435:11434`  
- Use `docker logs ollama` to debug issues  

---

## 3. Setup Open WebUI

Provides a ChatGPT-like interface for local models.

### Pull Image

```bash
docker pull ghcr.io/open-webui/open-webui:main
```

### Run Container

```bash
docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

### Access

http://localhost:3000

### Notes

- UI runs on port **3000**  
- Data is saved in Docker volume (`open-webui`)  
- If UI doesn’t open, check container:
  ```bash
  docker ps
  ```
- Restart using:
  ```bash
  docker restart open-webui
  ```

---

## 4. Add Models

Pull a model using Ollama:

```bash
ollama pull llama3
```

### Steps

- Open WebUI  
- Go to Admin Panel  
- Refresh models  
- Select model  

### Notes

- First model download can be **large (GBs)**  
- Requires good internet initially  
- After download, works offline  
- You can install other models:
  - `mistral`
  - `gemma`
  - `phi`

---
## 5. Ollama API

Ollama provides a simple REST API to interact with locally running LLMs.  
It allows you to send prompts and receive generated responses programmatically.

### Base Endpoint

```
http://localhost:11434/api/generate
```

You can use this endpoint in any backend or frontend application to generate responses from your local LLM.

### Notes

- Runs completely **locally** (no internet required after setup)  
- Works with any HTTP client (Python, JS, Postman, curl)  
- Make sure Ollama container is running before calling API  
- Default port: `11434`  

---

## 6. FastAPI Setup

FastAPI is a modern Python framework used to build fast and efficient APIs.  
It is widely used for AI and backend services due to its simplicity and performance.

### Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install "fastapi[standard]"
pip freeze > requirements.txt
```

### Run Application

```bash
fastapi dev file_name.py
```

### Example FastAPI App

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is running"}
```

### Notes

- Virtual environment keeps dependencies isolated  
- `requirements.txt` helps in reproducibility  
- Default FastAPI runs on: `http://127.0.0.1:8000`  
- Auto docs available at:
  - `/docs` (Swagger UI)  
  - `/redoc`  

---

## 7. Integrate Ollama with FastAPI

This step connects your FastAPI backend with the Ollama model server.  
It allows your API to send prompts to the model and return responses dynamically.

### Install Ollama Python Package

```bash
pip install ollama
```

### Example API Integration

```python
from fastapi import FastAPI
from pydantic import BaseModel
from ollama import Client

app = FastAPI()
client = Client(host="http://localhost:11434")

class PromptRequest(BaseModel):
    prompt: str
    model: str = "llama3"

@app.post("/chat")
def chat(data: PromptRequest):
    response = client.chat(
        model=data.model,
        messages=[
            {"role": "user", "content": data.prompt}
        ]
    )
    return {
        "response": response.message.content
    }
```

### Notes

- `Client` connects FastAPI with local Ollama server  
- `pydantic` ensures request validation  
- Model name can be changed dynamically  
- Supports multi-turn conversations  
- Useful for building AI-powered APIs  

---

## 8. Test API

Testing ensures your API is working correctly before integrating into applications.  
You can test using command-line tools or API testing platforms.

### Using curl

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d "{\"prompt\":\"Explain AI\",\"model\":\"llama3\"}"
```

### Notes

- Ensure FastAPI server is running before testing  
- Endpoint: `/chat`  
- Method: `POST`  
- You can also test using:
  - Browser (`/docs`)  
  - Postman  
  - Thunder Client (VS Code)  

---

## Conclusion (This Section)

You now have a complete pipeline from local model to API service.  
This setup enables you to build scalable AI applications fully offline.

- Ollama API access  
- FastAPI backend setup  
- Integrated local LLM with API  
- Tested endpoint successfully  

### Use Cases

- AI chatbots  
- Backend AI services  
- Full-stack AI applications  

## Summary

1. Install Docker  
2. Test Docker setup  
3. Run Ollama container  
4. Run Open WebUI  
5. Download models  
6. Use via UI or API  

---

## General Notes

- Ensure required ports are free:
  - `11434` → Ollama  
  - `3000` → WebUI  
- Use volumes to avoid data loss  
- Check running containers:
  ```bash
  docker ps
  ```
- Stop containers:
  ```bash
  docker stop ollama open-webui
  ```

---

## Conclusion

You now have a complete local LLM environment:

- Private AI system  
- Web-based interface  
- API for development  

### Use Cases

- Learning AI  
- Building projects  
- Offline chatbot systems  
- Secure/local data processing  