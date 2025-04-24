import os
import cmd

from infrastructure.gateway.envoy_gateway import EnvoyAIGateway
from domain.ports.gateway import AIGateway


class AIShell(cmd.Cmd):
    intro = "Welcome to the AI Platform shell. Type help or ? to list commands.\n"
    prompt = "ai> "

    def __init__(self, gateway: AIGateway):
        super().__init__()
        self.gateway = gateway

    def do_exit(self, _):
        """Exit the shell"""
        return True

    def do_chat(self, line):
        """chat <model> <message>"""
        try:
            model, *msg = line.split()
            message = " ".join(msg)
            response = self.gateway.chat(model=model, message=message)
            print(response)
        except Exception as e:
            print(f"Error: {e}")

    def do_stream(self, line: str):
        """stream <model> <message>"""
        try:
            model, *msg = line.split()
            message = " ".join(msg)
            for token in self.gateway.stream_chat(model, message):
                print(token, end='', flush=True)
            print()
        except Exception as e:
            print(f"Stream error: {e}")

    def do_EOF(self, _):
        return self.do_exit(_)


if __name__ == "__main__":
    gateway = EnvoyAIGateway(base_url=os.environ["AI_GATEWAY_HOST"])
    AIShell(gateway).cmdloop()
