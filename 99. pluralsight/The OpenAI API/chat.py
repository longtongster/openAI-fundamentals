import sys
import os
from openai import OpenAI

# Use current working directory and go one level up
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(parent_dir)

# Now you can import your config
from config import api_key


from openai import OpenAI
client = OpenAI(api_key=api_key)

message = "Write two sentences on how to release stress."

completion = client.chat.completions.create(
    model="gpt-4.1",
    temperature=0,
    messages=[
        {
            "role": "system",
            "content": "you are a writer of children books and use simple to understand words"
        },
        {
            "role": "user",
            "content": message
        },
    ]
)

print(completion.choices[0].message.content)