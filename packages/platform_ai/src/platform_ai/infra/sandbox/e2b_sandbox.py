from e2b_code_interpreter import Sandbox
from platform_ai.domain.ports.sandbox import Sandbox as SandboxProtocol


class E2BSandbox(SandboxProtocol):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def run_code(self, code: str, language: str = "python") -> None:
        with Sandbox() as sandbox:
            try:
                execution = sandbox.run_code(code)
                result = execution.logs.stdout
                print(result)
            except Exception as e:
                print("Exception", e)
            finally:
                sandbox.kill()
