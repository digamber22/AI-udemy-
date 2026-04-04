# Multimodal Image Input (URL + Base64)

This guide shows two ways to send images to an AI model:

1. Using an **Image URL**
2. Using a **Local File (Base64 encoding)**

---

## 1) Using Image URL

This is the easiest way when your image is hosted online.

### Example (Python)

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Generate a caption for this image in about 50 words"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://images.pexels.com/photos/879109/pexels-photo-879109.jpeg"
                    }
                }
            ]
        }
    ]
)

print("Response:", response.choices[0].message.content)
```
# 

# Complete Base64 Workflow (Encode → Send → Decode)

This is the **full working code** for handling a local image using Base64:

- Encode local file  
- Send to AI model  
- Decode back to file  

---

## Full Example (Python)

```python
from openai import OpenAI
import base64

# Initialize client
client = OpenAI()

# -----------------------------
# Step 1: Encode Image to Base64
# -----------------------------
with open("image.png", "rb") as file:
    encoded = base64.b64encode(file.read()).decode("utf-8")

print("Encoded successfully")

# -----------------------------
# Step 2: Send Base64 to Model
# -----------------------------
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in detail"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encoded}"
                    }
                }
            ]
        }
    ]
)

print("AI Response:")
print(response.choices[0].message.content)

# -----------------------------
# Step 3: Decode Base64 to File
# -----------------------------
with open("output.png", "wb") as file:
    file.write(base64.b64decode(encoded))

print("Decoded and saved as output.png")