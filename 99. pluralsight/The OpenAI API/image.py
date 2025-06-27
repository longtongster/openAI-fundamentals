from openai import OpenAI
import sys
import os
import base64

# Use current working directory and go one level up
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(parent_dir)

# Now you can import your config
from config import api_key

client = OpenAI(api_key=api_key)

response = client.images.generate(
    model="dall-e-3",
    prompt="A cute white baby cat",
    n=1,
    size="1024x1024",
    response_format="b64_json")

# print(response)

for i, image in enumerate(response.data):
    image_data=base64.b64decode(image.b64_json)

    with open(f"image_{i}.png", "wb") as f:
              f.write(image_data)
              
