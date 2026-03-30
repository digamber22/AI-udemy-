## 🛠️ Python Virtual Environment Setup & Execution of tokenization in python

```bash
# Create a virtual environment named "venv"
python -m venv venv

# Activate the virtual environment (Linux / Mac)
source venv/bin/activate

# Install required package (tokenization library)
pip install tiktoken

# Save all installed dependencies into requirements.txt
pip freeze > requirements.txt

# Run the Python script (after going to dir)
python main.py