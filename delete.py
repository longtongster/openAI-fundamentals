
def add_numbers(a, b):
    return a + b

from crewai import Agent
from langchain.tools import Tool
from langchain.agents import load_tools
import subprocess
import sys

class CodeInterpreterTool:
    def __init__(self):
        # Ensure scikit-learn is installed
        try:
            import sklearn
        except ImportError:
            print("Installing scikit-learn...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn"])

    def execute_code(self, code: str) -> str:
        """Execute the provided Python code and return the output"""
        try:
            # Create a local namespace for execution
            local_namespace = {}
            exec(code, globals(), local_namespace)
            return str(local_namespace.get('result', 'Code executed successfully'))
        except Exception as e:
            return f"Error executing code: {str(e)}"

# Create the code interpreter tool
code_tool = CodeInterpreterTool()

# Create the tool for the agent
code_execution_tool = Tool(
    name="Code Executor",
    func=code_tool.execute_code,
    description="Executes Python code and returns the output. The code should be provided as a string."
)

# Create the coding agent
coding_agent = Agent(
    role='Python Programmer',
    goal='Write and execute Python code with scikit-learn',
    backstory='I am an AI agent specialized in writing and executing Python code, particularly for machine learning tasks using scikit-learn.',
    tools=[code_execution_tool],
    verbose=True,
    allow_delegation=False
)