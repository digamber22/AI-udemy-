# Torch and Important AI Terms (Quick Notes)

This guide explains important terms used in AI/ML, Hugging Face, and local LLMs.
It helps you understand how models work internally and how different tools connect together.

---

## 1. Torch (PyTorch)

Torch (PyTorch) is a deep learning framework used to build and run AI models.
It acts as the computation engine that processes data and generates outputs.

### Key Points

* Works with tensors (multi-dimensional arrays)
* Runs neural networks
* Supports CPU and GPU
* Used by most modern AI models

### Example

```python
import torch
x = torch.tensor([1, 2, 3])
print(x)
```

---

## 2. Transformers

Transformers is a Python library used to load and use pretrained models easily.
It provides a simple interface to run complex AI models.

### Example

```python
from transformers import pipeline
pipe = pipeline("text-generation", model="distilgpt2")
print(pipe("Hello AI"))
```

---

## 3. Model

A model is a trained AI system that can perform tasks like text generation or classification.
It contains learned knowledge from training data.

### Examples

* distilgpt2
* bert-base-uncased
* gemma

---

## 4. Tokenizer

A tokenizer converts text into numbers so that models can understand it.
Since models work with numbers, this step is required before processing input.

### Example

```python
tokens = tokenizer("Hello world")
```

---

## 5. Pipeline

Pipeline is a high-level API that simplifies using models.
It automatically handles model loading, tokenization, and inference.

### Example

```python
pipe = pipeline("text-generation")
```

---

## 6. Inference

Inference means using a trained model to generate output.
It is different from training because no learning happens here.

### Example

```python
pipe("What is AI?")
```

---

## 7. Training

Training is the process of teaching a model using data.
It involves adjusting weights based on errors.

---

## 8. Checkpoint

A checkpoint is a saved version of a trained model.
It includes configuration and learned weights.

### Files

* config.json
* model.safetensors

---

## 9. Weights

Weights are the learned parameters of a model.
They store the knowledge gained during training.

---

## 10. Dataset

A dataset is a collection of data used to train or test a model.
It can include text, images, or audio.

---

## 11. CPU vs GPU

CPU and GPU are hardware used to run models.

### Comparison

* CPU → slower, general purpose
* GPU → faster, used for AI computations

---

## 12. Multimodal

Multimodal models can understand multiple types of data like text and images.
They are more advanced but usually larger in size.

---

## 13. Embeddings

Embeddings convert text into numerical vectors.
They are used for search, similarity, and recommendation systems.

---

## 14. Hugging Face Hub

Hugging Face Hub is a platform where models are stored and shared.
It is like GitHub but for AI models.

---

## 15. Gated Models

Gated models require permission before use.
You must accept their license or request access.

---

## 16. Virtual Environment (venv)

A virtual environment isolates project dependencies.
It helps avoid conflicts between different projects.

### Example

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## 17. Requirements.txt

A file that stores all installed packages.
It helps recreate the same environment later.

### Example

```bash
pip freeze > requirements.txt
```

---

## 18. Hugging Face CLI

CLI tools allow you to interact with Hugging Face from the terminal.
Used for login, downloading models, and managing access.

### Example

```bash
hf auth login
```

---

## 19. Prompt

A prompt is the input text given to the model.
The quality of the prompt affects the quality of the output.

### Example

```text
Explain AI in simple words
```

---

## 20. Prompt Engineering

Prompt engineering is the skill of writing better prompts to get better answers from models.
It is very useful when working with chatbots and LLMs.

### Notes

* Clear prompts give better results
* You can ask for steps, summaries, or examples
* Small changes in prompt can change output a lot

---

## 21. LLM (Large Language Model)

An LLM is a large model trained on huge amounts of text data.
It can understand and generate human-like language.

### Examples

* Llama
* Mistral
* Gemma
* GPT-style models

---

## 22. Context Window

The context window is the amount of text a model can remember at one time.
If the conversation becomes too long, older text may be ignored.

### Notes

* Bigger context means the model can handle more text
* Very important in chat applications
* Useful for long documents and conversations

---

## 23. Fine-Tuning

Fine-tuning means taking a pretrained model and training it a little more on your own data.
It helps the model perform better on a specific task.

### Notes

* Saves time compared to training from scratch
* Used for custom chatbots and domain-specific AI
* Needs dataset and training setup

---

## 24. Parameters

Parameters are the internal values learned by the model during training.
They decide how the model behaves and makes predictions.

### Notes

* More parameters usually mean a larger model
* Parameters store learned knowledge
* Model size is often measured by parameter count

---

## 25. Hyperparameters

Hyperparameters are settings chosen before training starts.
Examples are learning rate, batch size, and number of epochs.

### Notes

* They are not learned by the model
* They are set by the developer
* They strongly affect training quality

---

## 26. Learning Rate

Learning rate controls how fast the model updates during training.
If it is too high or too low, training may not work well.

### Notes

* Small learning rate → slow training
* Large learning rate → unstable training
* Very important in deep learning

---

## 27. Epoch

One epoch means the model has seen the full dataset once during training.
Training usually runs for many epochs.

### Notes

* More epochs can improve learning
* Too many epochs can cause overfitting
* Used in model training loops

---

## 28. Batch Size

Batch size is the number of samples used before the model updates its weights.
It helps balance speed and memory usage.

### Notes

* Small batch size uses less memory
* Large batch size can be faster on GPU
* Common training term in deep learning

---

## 29. Loss Function

A loss function measures how wrong the model’s prediction is.
Training tries to reduce this loss.

### Notes

* Lower loss means better prediction
* Used during training
* Helps the model learn from mistakes

---

## 30. Optimizer

An optimizer updates the model weights to reduce loss.
It is a key part of the training process.

### Notes

* Common optimizers: Adam, SGD
* Works together with loss function
* Helps the model learn efficiently

---

## 31. Overfitting

Overfitting happens when a model learns the training data too well and performs badly on new data.
It means the model memorized instead of generalized.

### Notes

* Common training problem
* Can be reduced using more data, regularization, or early stopping

---

## 32. Underfitting

Underfitting happens when a model is too simple to learn the pattern in the data.
It performs poorly even on training data.

### Notes

* Model has not learned enough
* May need more training or a better model

---

## 33. Quantization

Quantization reduces the precision of model weights to make models smaller and faster.
It is often used in local LLMs.

### Notes

* Saves memory
* Helps run big models on smaller devices
* Common in deployment

---

## 34. LoRA

LoRA is a method used to fine-tune large models efficiently.
It updates only a small part of the model instead of all weights.

### Notes

* Uses less memory
* Faster than full fine-tuning
* Popular for custom AI projects

---

## 35. RAG (Retrieval-Augmented Generation)

RAG is a method where the model first retrieves useful information and then generates an answer.
It helps the model answer with external knowledge.

### Notes

* Useful for document-based chatbots
* Combines search + generation
* Very important in modern AI systems

---

## 36. Vector Database

A vector database stores embeddings and helps search similar items quickly.
It is commonly used in RAG systems.

### Notes

* Stores numerical vectors
* Used for semantic search
* Helpful in AI assistants

---

## 37. API

An API allows one program to talk to another program.
In AI, APIs are used to send prompts to models and get responses.

### Notes

* Used in backend and frontend apps
* Makes AI integration easy
* Ollama and FastAPI both use APIs

---

## 38. Local LLM

A local LLM is a model that runs on your own machine instead of a cloud server.
It gives more privacy and control.

### Notes

* Works offline after setup
* Good for learning and experiments
* Example tools: Ollama, Open WebUI

---

## 39. Inference Server

An inference server is a system that serves model predictions through an API.
It runs the model and gives outputs to users or apps.

### Notes

* Used in deployment
* Can serve multiple requests
* Ollama can act like an inference server

---

## 40. Big Picture

```text
Dataset → Training → Model → Tokenizer → Inference → Output
```

### Extended Flow

```text
Dataset → Training → Checkpoint → Fine-Tuning → Inference → API → App
```

---

## Summary

* Torch → runs models
* Transformers → easy interface
* Model → AI brain
* Tokenizer → converts text to numbers
* Pipeline → shortcut to use models
* GPU → speeds up computation
* Prompt → input to model
* Fine-tuning → custom training
* RAG → adds external knowledge
* Quantization → makes model smaller
* LoRA → efficient fine-tuning
* Vector DB → stores embeddings
* API → connects model to app

---

## Conclusion

These terms form the foundation of working with AI models.
Understanding them will help you build projects, debug issues, and learn advanced topics like RAG, fine-tuning, local LLMs, and AI deployment.