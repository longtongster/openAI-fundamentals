from crewai_tools import CodeInterpreterTool
from crewai import Agent, Task, Crew

import sys
import os

# Use current working directory and go one level up
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(parent_dir)

# Now you can import your config
from config import api_key, serper_api_key

import os

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'
os.environ["OPENAI_API_KEY"] = api_key


# Initialize the CodeInterpreterTool with your custom image
code_tool = CodeInterpreterTool(user_dockerfile_path='./docker/Dockerfile')

# Create an agent with the tool
agent = Agent(
	tools=[code_tool],
    allow_code_execution=True,
	name="Code Agent",
	role="Developer",  # Required field
	goal="Run code in custom Docker image",  # Required field
	backstory="This agent is designed to verify scikit-learn access in a custom Docker image.",  # Required field
	description="Agent to run code in custom Docker image"
)

# Create a task for the agent to check sklearn version
task = Task(
	agent=agent,
	description="1. Tell me what docker image you are using. 2. Check scikit-learn version in Docker image",
	input="import sklearn; print(sklearn.__version__)",
	expected_output="The version number of scikit-learn installed in the Docker image."
)


# Create a minimal Crew and run the task
crew = Crew(
	agents=[agent],
	tasks=[task],
	verbose=True
)

results = crew.kickoff()
print(results)

