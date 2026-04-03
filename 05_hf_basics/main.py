from transformers import pipeline

# text model (small ~250MB)
text_pipe = pipeline("text-generation", model="distilgpt2")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]

# extract text from message
question = messages[0]["content"][1]["text"]

# since distilgpt2 can't see image, we simulate context
prompt = f"""
A candy wrapper has an image of a bear on it.
Question: {question}
Answer:
"""

result = text_pipe(prompt, max_length=50)

print(result[0]["generated_text"])