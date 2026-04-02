from dotenv import load_dotenv   # loads environment variables from .env file
from openai import OpenAI       # imports OpenAI client class

load_dotenv()                   # reads .env file and stores variables in environment

client = OpenAI()               # creates client object (API key auto-loaded from env)
                                # NOTE: 'client' can be renamed, but 'OpenAI' cannot

response = client.chat.completions.create(   # sends request to OpenAI chat model
    model="gpt-4o-mini",                     # defines which model to use
    messages=[                               # list of conversation messages
        {
            "role": "user",                   # role = who is sending message
            "content": "Hey, I am Piyush Garg! Nice to meet you"   # actual input text
        }
    ]
)

print(response.choices[0].message.content)    # prints AI-generated response


'''
STEPS TO RUN PROJECT:

1) python -m venv venv
   # create virtual environment

2) .\venv\Scripts\activate.ps1
   # activate virtual environment (Windows PowerShell)

3) pip install openai python-dotenv
   # install required libraries

4) pip freeze > requirements.txt
   # save dependencies for future use

5) create .env file and add:
   # OPENAI_API_KEY=your_api_key_here

6) python file_name
   # run the script
'''