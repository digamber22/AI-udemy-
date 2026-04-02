# Prompting Techniques Overview

## 1. Zero-Shot Prompting
Asking the AI to perform a task without providing any prior examples. The model relies entirely on its pre-trained knowledge to generate the answer.
* **Best for:** Simple, common, or straightforward tasks.
* **Example:** *"Classify the sentiment of this sentence: 'I am happy.'"*

## 2. One-Shot Prompting
Providing exactly **one** example of the desired input and output before asking the AI to complete the target task. 
* **Best for:** Establishing a specific format, tone, or style quickly.
* **Example:** > Sentence: "I hate this." | Sentiment: Negative
  > Sentence: "This is wonderful!" | Sentiment:

## 3. Few-Shot Prompting
Providing **multiple** examples (usually 2 to 5+) of inputs and outputs to demonstrate a specific pattern, logic, or complex formatting.
* **Best for:** Complex reasoning, strict output constraints, or teaching the model a novel task.
* **Example:**
  > English: Cat -> Spanish: Gato
  > English: Dog -> Spanish: Perro
  > English: Bird -> Spanish: Pájaro
  > English: Horse -> Spanish:

#
  # Quick Summary: LLM Prompt Serialization & Formats

**Prompt Serialization** is the process of converting structured chat data (e.g., JSON message arrays) into a single, continuous text string. It uses specific templates and tokens so the LLM knows exactly who is speaking (System, User, or Assistant) and when.

### The 3 Major Formats Compared

| Format | Origin / Standard | Delimiters Used | Best For | Key Advantage |
| :--- | :--- | :--- | :--- | :--- |
| **Alpaca** | Stanford | `### Instruction:`<br>`### Response:` | Basic instruction-tuning | Simple, plain-text structure. Great for early or basic single-turn models. |
| **ChatML** | OpenAI | `<|im_start|>`<br>`<|im_end|>` | Complex, multi-turn chat | Security. Uses strict special tokens at the tokenizer level to prevent prompt injection. |
| **[INST]** | Meta (LLaMA), Mistral | `[INST]`<br>`<<SYS>>` | Modern open-source models | The current industry standard for structuring complex chats in state-of-the-art open-weights models. |