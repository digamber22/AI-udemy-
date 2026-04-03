# Installation and Using of Hugging Face CLI Tools and Transformers

This guide explains how to set up Hugging Face CLI tools and use the `transformers` package in Python.

The goal is to create a simple workflow where you can:

* Log in to Hugging Face
* Accept access for gated models
* Use pretrained models in Python
* Save dependencies for future use

---

## 1. Install Hugging Face Hub CLI Tools

Hugging Face CLI tools help you log in, manage access, and work with models from the terminal.
They are useful when you want to download gated models or connect your local system with your Hugging Face account.

### Create and Activate Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install Hugging Face Hub

```bash
pip install -U huggingface_hub
```

### Login to Hugging Face

```bash
hf auth login
```

### Meaning

* `python -m venv venv` → creates a virtual environment
* `Activate.ps1` → activates the environment in Windows PowerShell
* `pip install -U huggingface_hub` → installs Hugging Face Hub tools
* `hf auth login` → logs in to your Hugging Face account

### Notes

* Use a virtual environment for clean dependency management
* The CLI is useful for downloading models and handling access
* Always activate the environment before installing packages
* If login asks for a token, paste your Hugging Face access token

---

## 2. Get Hugging Face Access Token

The access token works like a login key for Hugging Face.
It is required when you want to authenticate your terminal and access private or gated models.

### Steps

* Open your Hugging Face dashboard
* Go to **Access Tokens**
* Click **New token**
* Choose a token name
* Select **write** access if you want full model management
* Copy the token and paste it during `hf auth login`

### Notes

* The token is sensitive, so keep it private
* Use **read** access for downloading models only
* Use **write** access if you need upload or management permissions
* You can generate a new token anytime from your account settings

---

## 3. Accept License for Gated Models

Some models are gated, which means Hugging Face asks you to accept their license or request access before using them.
This is common for large or restricted models like `gemma-3n-E4B-it`.

### Example

* Search the model in your browser
* Open the model page
* Accept the license or request access
* Wait for approval if needed
* Then use it from Python

### Notes

* Gated models cannot be used until access is granted
* Browser approval is often required before downloading
* Login with `hf auth login` helps your terminal use the same account
* Once access is approved, you can load the model in code

---

## 4. Install Transformers

`transformers` is the Python package used to load and run pretrained AI models.
It is useful for text generation, classification, translation, and many other AI tasks.

### Install Package

```bash
pip install transformers
```

### Meaning

* `pip install transformers` → installs the Transformers library

### Notes

* Transformers is the main library for working with Hugging Face models
* It works with pretrained models from the Hugging Face Hub
* You can use it in text, image, and multimodal projects
* Install it inside the virtual environment for better control

---

## 5. Use Transformers in Python

Transformers lets you load models in Python with very little code.
It is useful because you can run pretrained models without building one from scratch.

### Example Code

```python
from transformers import pipeline

pipe = pipeline("text-generation", model="distilgpt2")
result = pipe("Hello, my name is", max_length=30)
print(result)
```

### Notes

* `pipeline()` gives a simple way to run a model
* `distilgpt2` is a small text-generation model
* The model will be downloaded the first time you run it
* Later runs will be faster because files stay cached

---

## 6. Save Installed Packages

Saving dependencies helps you recreate the same environment later.
This is useful when you share your project or run it again on another computer.

### Save Requirements

```bash
pip freeze > requirements.txt
```

### Notes

* `requirements.txt` stores installed package versions
* It helps you reinstall the same setup later
* It is useful for project sharing and deployment
* Run this after installing the packages you need

---

## 7. Run Your Python File

This command runs your Python program from the terminal.
It is the final step after installing packages and writing your script.

### Run File

```bash
python file_name.py
```

### Notes

* Replace `file_name.py` with your actual Python file
* Make sure the virtual environment is active
* Run the file from the correct project folder
* If the model is large, the first run may take time

---

## 8. Useful Workflow Summary

First create and activate the virtual environment, then install `huggingface_hub` and `transformers`.
After that, log in with your token, accept model access if needed, save dependencies, and run your Python file.

### Full Setup Flow

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -U huggingface_hub
hf auth login
pip install transformers
pip freeze > requirements.txt
python main.py
```

### Notes

* This is the recommended project workflow
* Keep every package inside the same environment
* Use the browser for gated model access
* Use the terminal for login and Python execution

---

## 9. Important Notes

* Use a virtual environment for every project
* Use `hf auth login` to connect your account
* Use your access token instead of a password
* Accept model licenses in the browser before using gated models
* `transformers` is used to load and run AI models in Python

---

## Conclusion

You now have a complete basic setup for Hugging Face CLI tools and Transformers.
This setup helps you log in, access models, run pretrained AI models, and manage dependencies in a clean way.

### Use Cases

* Downloading Hugging Face models
* Accessing gated models
* Running AI models in Python
* Building small NLP projects
* Saving project dependencies for future use

## Summary

1. Create and activate virtual environment
2. Install `huggingface_hub`
3. Login with Hugging Face token
4. Accept model access in browser
5. Install `transformers`
6. Run model in Python
7. Save dependencies in `requirements.txt`
8. Execute your script with `python file_name.py`

---

## General Notes

* Keep your token private
* Use `requirements.txt` for reproducibility
* Run everything inside the virtual environment
* Check model access before trying to use gated models
* Start with small models like `distilgpt2` for learning

---

## Conclusion

You now have a simple Hugging Face workflow:

* CLI login
* Token authentication
* Gated model access
* Transformers model loading
* Python script execution