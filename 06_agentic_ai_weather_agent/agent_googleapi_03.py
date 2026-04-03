from dotenv import load_dotenv
from google import genai
import requests
from pydantic import BaseModel, Field
from typing import Optional
import json
import os

# ==============================
# SETUP
# ==============================

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# ==============================
# TOOLS
# ==============================

def run_command(cmd: str):
    return os.system(cmd)

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

# ==============================
# SYSTEM PROMPT
# ==============================

SYSTEM_PROMPT = """
You're an AI agent.

Follow steps:
START → PLAN → TOOL → OUTPUT

Rules:
- Always return ONLY JSON (no markdown, no explanation)
- One step at a time
- If using a tool, step MUST be "TOOL"
- Never include tool inside PLAN

Format:
{ "step": "...", "content": "...", "tool": "...", "input": "..." }

Available Tools:
- get_weather(city)
- run_command(cmd)
"""

# ==============================
# OUTPUT STRUCTURE
# ==============================

class MyOutputFormat(BaseModel):
    step: str
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None

# ==============================
# MEMORY
# ==============================

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

# ==============================
# MAIN LOOP
# ==============================

while True:
    user_query = input("👉🏻 ")

    message_history.append({"role": "user", "content": user_query})

    while True:

        # Gemini call
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[msg["content"] for msg in message_history]
        )

        raw_result = response.text

        # Save response
        message_history.append({"role": "assistant", "content": raw_result})

        # ==============================
        # CLEAN JSON (IMPORTANT FIX)
        # ==============================

        cleaned = raw_result.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()

        # ==============================
        # PARSE JSON
        # ==============================

        try:
            parsed_result = MyOutputFormat.model_validate_json(cleaned)
        except Exception:
            print("❌ Invalid JSON from model:", raw_result)
            break

        # ==============================
        # HANDLE STEPS
        # ==============================

        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue

        if parsed_result.step == "PLAN":
            print("🧠", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_name = parsed_result.tool
            tool_input = parsed_result.input

            print(f"🛠️ Calling Tool: {tool_name}({tool_input})")

            try:
                tool_response = available_tools[tool_name](tool_input)
            except Exception as e:
                tool_response = str(e)

            print(f"🛠️ Tool Result: {tool_response}")

            # Send OBSERVE back
            message_history.append({
                "role": "user",
                "content": json.dumps({
                    "step": "OBSERVE",
                    "tool": tool_name,
                    "input": tool_input,
                    "output": tool_response
                })
            })

            continue

        if parsed_result.step == "OUTPUT":
            print("🤖", parsed_result.content)
            break