from google import genai
from dotenv import load_dotenv
import os
import requests

# Load .env
load_dotenv()

# API key
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Weather function
def get_weather(city):
    url = f"https://wttr.in/{city}?format=%C+%t"
    res = requests.get(url)
    return res.text

# Main
user_query = input("> ")

# Simple condition
if "weather" in user_query.lower():
    city = user_query.split("in")[-1].strip()
    print(get_weather(city))
else:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_query
    )
    print(response.text)