import requests
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.live import Live
from time import sleep

console = Console()
ENVOY_URL = "http://localhost:8080/agent1"

chat_history = []

def send_message_to_agent(message):
    try:
        response = requests.post(ENVOY_URL, json={"message": message}, timeout=30)
        if response.ok:
            return response.json().get("response", "[No response field]")
        else:
            return f"[Error {response.status_code}] {response.text}"
    except Exception as e:
        return f"[Error] {str(e)}"


def render_chat():
    rendered = ""
    for entry in chat_history:
        sender, text = entry
        prefix = "[bold green]You:[/bold green]" if sender == "user" else "[bold cyan]Agent:[/bold cyan]"
        rendered += f"{prefix} {text}\n\n"
    return Panel(rendered.strip(), title="🤖 AI Gateway Chat", padding=(1, 2))


def run_chat():
    console.clear()
    console.print(render_chat())
    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
            if user_input.strip().lower() == "exit":
                break

            chat_history.append(("user", user_input))
            with Live(render_chat(), refresh_per_second=4, console=console):
                spinner = Spinner("dots", text="Agent is thinking...")
                console.print(spinner)
                reply = send_message_to_agent(user_input)
                sleep(0.5)  # simulate delay

            chat_history.append(("agent", reply))
            console.clear()
            console.print(render_chat())
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    run_chat()