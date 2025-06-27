import sys
import os
from openai import OpenAI

# Use current working directory and go one level up
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(parent_dir)

# Now you can import your config
from config import api_key

client = OpenAI(api_key=api_key)
audio_file= open("Recording.m4a", "rb")

print("Start transcription - audio will be send via the api and the transcription will be in the response")

transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file,
    language="nl",  # Dutch language hint
    prompt="De spreker heet Sacha. Hij spreekt vloeiend Nederlands."  # Light context

)

print(transcription.text)