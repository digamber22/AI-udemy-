```python
# openai_hello.py
# need to .env file for openai api key 

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        { "role": "user", "content": "Hey, I am Piyush Garg! Nice to meet you"}
    ]
)

print(response.choices[0].message.content)
```

```python
# gemini_hello.py 
# without .evn file  (not recommended practice)

from google import genai

client = genai.Client(
    api_key="AIzaSyDYPCDzhpraniZXsOPXnb2JAv3P7JSCwvg"
)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)

print(response.text)
```

```python
# gemini_openai.py
# Flexibility:
  # → Same code can work for OpenAI, Gemini, Groq
  # → Just change api_key + base_url + model

  from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="AIzaSyBjA34ENgeGNplvIqCP-qcH2fuMkqxdO7o",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": "You are an expert in Maths and only and only ans maths realted questions. That if the query is not related to maths. Just say sorry and do not ans that." },
        { "role": "user", "content": "Hey, can you help me solve the a + b whole square"}
    ]
)

print(response.choices[0].message.content)
```
#
## 🚀 Project Setup & Run Guide

### 1️⃣ Create Virtual Environment
    python -m venv venv
Creates an isolated environment for your project.

### 2️⃣ Activate Virtual Environment (Windows PowerShell)
    .\venv\Scripts\activate.ps1
Activates the environment so all dependencies install locally.

### 3️⃣ Install Required Packages
    pip install openai python-dotenv
Installs required libraries:
- openai → OpenAI SDK  
- python-dotenv → Load environment variables  

### 4️⃣ Save Dependencies (Optional but Recommended)
    pip freeze > requirements.txt
Saves all installed packages for reuse.

### 5️⃣ Configure Environment Variables
Create a `.env` file in your project root and add:
    OPENAI_API_KEY=your_api_key_here
Keeps your API key secure and separate from code.

### 6️⃣ Run the Application
    python file_name.py
Runs your Python script.

---

## 📌 Notes
- Always activate the virtual environment before running the project.
- Do NOT share your `.env` file publicly (add it to `.gitignore`).
- To recreate environment on another system:
    pip install -r requirements.txt

---
