# AI Agent Project

## File: main.py

```python
from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

client = OpenAI()

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"


def main():
    user_query = input("> ")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            { "role": "user", "content": user_query }
        ]
    )

    print(f"🤖: {response.choices[0].message.content}")

main()
```

#

# File: agent.py

```python
from dotenv import load_dotenv
from openai import OpenAI
import requests
from pydantic import BaseModel, Field
from typing import Optional
import json
import os

load_dotenv()

client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result


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


SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.
You can also call a tool if required from the list of available tools.
For every tool call wait for the observe step which is the output from the called tool.

Rules:
- Strictly Follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START, PLAN and finally OUTPUT.

Output JSON Format:
{ "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

Available Tools:
- get_weather(city: str)
- run_command(cmd: str)
"""

class MyOutputFormat(BaseModel):
    step: str = Field(...)
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None


message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    user_query = input("👉🏻 ")
    message_history.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.parse(
            model="gpt-4o",
            response_format=MyOutputFormat,
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})
        
        parsed_result = response.choices[0].message.parsed

        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"🛠️: {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🛠️: {tool_to_call} ({tool_input}) = {tool_response}")

            message_history.append({
                "role": "developer",
                "content": json.dumps({
                    "step": "OBSERVE",
                    "tool": tool_to_call,
                    "input": tool_input,
                    "output": tool_response
                })
            })
            continue

        if parsed_result.step == "PLAN":
            print("🧠", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("🤖", parsed_result.content)
            break
    
```