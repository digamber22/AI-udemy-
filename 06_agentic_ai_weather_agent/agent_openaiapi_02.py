
from dotenv import load_dotenv      # Load environment variables (API keys, etc.)
from openai import OpenAI           # OpenAI client
import requests                     # For API calls (weather)
from pydantic import BaseModel, Field  # For structured output validation
from typing import Optional
import json
import os

load_dotenv()

# Create OpenAI client
client = OpenAI()


# ==============================
# TOOL FUNCTIONS
# ==============================

# Tool 1: # Tool 1: Runs terminal commands (used for CLI-based coding assistant like claude , cursor etc )
def run_command(cmd: str):
    # Executes a command in terminal (Linux/Windows)
    result = os.system(cmd)
    return result   # returns exit code (not output)

# Tool 2: Get weather info
def get_weather(city: str):
    # Using wttr.in free API
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"


# ==============================
# TOOL MAPPING
# ==============================

# This dictionary connects tool name → function
available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}


# ==============================
# SYSTEM PROMPT (AI INSTRUCTIONS)
# ==============================

SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.

You must follow steps:
START → PLAN → TOOL (if needed) → OUTPUT

Rules:
- Always return JSON format
- Only one step at a time
- You can call tools if required
- After tool call, wait for OBSERVE

Format:
{ "step": "...", "content": "...", "tool": "...", "input": "..." }

Available Tools:
- get_weather(city)
- run_command(cmd)
"""


# ==============================
# OUTPUT FORMAT STRUCTURE
# ==============================

# This ensures model returns structured JSON
class MyOutputFormat(BaseModel):
    step: str = Field(..., description="Step type (PLAN, TOOL, OUTPUT)")
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None


# ==============================
# MESSAGE HISTORY (MEMORY)
# ==============================

# Stores conversation history
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


# ==============================
# MAIN CHAT LOOP
# ==============================

while True:
    # Take input from user
    user_query = input("👉🏻 ")

    # Add user message to history
    message_history.append({"role": "user", "content": user_query})

    # Inner loop for multi-step reasoning
    while True:

        # Send conversation to model and parse structured output
        response = client.chat.completions.parse(
            model="gpt-4o",
            response_format=MyOutputFormat,
            messages=message_history
        )

        # Raw JSON string from model
        raw_result = response.choices[0].message.content

        # Save assistant response in history
        message_history.append({"role": "assistant", "content": raw_result})

        # Parsed object (easy to access fields)
        parsed_result = response.choices[0].message.parsed


        # ==============================
        # HANDLE DIFFERENT STEP TYPES
        # ==============================

        # START (optional)
        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue

        # PLAN (thinking step)
        if parsed_result.step == "PLAN":
            print("🧠", parsed_result.content)
            continue

        # TOOL CALL
        if parsed_result.step == "TOOL":
            tool_name = parsed_result.tool
            tool_input = parsed_result.input

            print(f"🛠️ Calling Tool: {tool_name}({tool_input})")

            # Execute tool function
            tool_response = available_tools[tool_name](tool_input)

            print(f"🛠️ Tool Result: {tool_response}")

            # Send tool result back to model as OBSERVE step
            message_history.append({
                "role": "developer",
                "content": json.dumps({
                    "step": "OBSERVE",
                    "tool": tool_name,
                    "input": tool_input,
                    "output": tool_response
                })
            })

            continue

        # FINAL OUTPUT
        if parsed_result.step == "OUTPUT":
            print("🤖", parsed_result.content)
            break


# ==============================
# END OF PROGRAM
# ==============================