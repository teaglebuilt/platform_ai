from crewai.tools import tool
from e2b_code_interpreter import Sandbox


@tool("Python Interpreter")
def execute_code(code: str):
    with Sandbox() as sandbox:
        execution = sandbox.run_code(code)
        return execution.text
