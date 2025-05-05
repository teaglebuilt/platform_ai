from platform_ai.domain.ports.gateway import AIGateway


class ChatWithAgent:
    def __init__(self, ai_gateway: AIGateway):
        self.ai_gateway = ai_gateway

    def execute(self, agent_name: str, message: str) -> str:
        return self.ai_gateway.chat(agent_name, message)
