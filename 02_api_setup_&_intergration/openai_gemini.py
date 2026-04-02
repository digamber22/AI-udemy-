# ================== IMPORTS ==================
from dotenv import load_dotenv        # load environment variables from .env (optional)
from openai import OpenAI             # import OpenAI SDK (client library)

# ================== LOAD ENV ==================
load_dotenv()                         # loads variables from .env file (if present)


# ================== CLIENT SETUP ==================
client = OpenAI(
    api_key="Google_Gemini_API",         # Google Gemini API key (not OpenAI key)
    base_url="https://generativelanguage.googleapis.com/v1beta/"  # search "gemini openai compatible api" in browser
    # base_url redirects request to Google Gemini instead of OpenAI
)


# ================== API CALL ==================
response = client.chat.completions.create(
    model="gemini-2.5-flash",         # Gemini model (not OpenAI model)
    messages=[
        {
            "role": "system",         # system message = sets behavior of AI
            "content": "You are a math expert. Only answer math-related questions. If not math, say sorry."
        },
        {
            "role": "user",           # user message = actual query
            "content": "Hey, can you help me solve the (a + b)^2"
        }
    ]
)


# ================== OUTPUT ==================
print(response.choices[0].message.content)   # print model's reply



"""
================== IMPORTANT NOTES ==================

1) This code uses OpenAI SDK but NOT OpenAI API.
   → It uses Google Gemini API via base_url.

2) api_key:
   → Must be a Google API key (starts with AIza...)
   → OpenAI keys start with "sk-"

3) base_url:
   → Decides which provider you are using
   → OpenAI (default) → no base_url needed
   → Gemini → use Google URL
   → Groq → use Groq URL

4) SDK vs API:
   → OpenAI() = SDK (tool/client)
   → base_url = actual API provider

5) messages:
   → system = behavior instructions
   → user = actual question
   → assistant = model reply (returned)

6) model:
   → "gemini-2.5-flash" = Google Gemini model
   → Not an OpenAI model

7) Security Warning:
   → Do NOT hardcode API keys in real projects
   → Use .env file instead

8) Flexibility:
   → Same code can work for OpenAI, Gemini, Groq
   → Just change api_key + base_url + model

9) Error you faced earlier (429):
   → That happens only with OpenAI (quota issue)
   → Gemini works with its own limits

=====================================================
"""