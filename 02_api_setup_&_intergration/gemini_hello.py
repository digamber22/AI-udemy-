from google import genai

client = genai.Client(
    api_key="google gemini api key"
)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words and what is genai and what is different between genai and agentic ai "
)

print(response.text)




"""
================== STEPS TO RUN ==================
this code is without .evn file and in openai wale with .env 

1) Create virtual environment:
   python -m venv venv

2) Activate (Windows PowerShell):
   .\venv\Scripts\activate.ps1

3) Install dependencies:
   pip install google-genai python-dotenv

4) (Optional but recommended):
   pip freeze > requirements.txt

5) (Optional for security) Create .env file:
   GEMINI_API_KEY=your_api_key_here

6) Run the script:
   python gemini_hello.py

=================================================
"""