import requests

ENVOY_URL = "http://localhost:8080/agent1"

def send_message_to_agent(message):
    try:
        response = requests.post(ENVOY_URL, json={"message": message})
        if response.ok:
            return response.json().get("response", "[No response field]")
        else:
            return f"[Error {response.status_code}] {response.text}"
    except Exception as e:
        return f"[Error] {e}"


def run_chat():
    print("=== AI Gateway Terminal Chat ===")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break

        reply = send_message_to_agent(user_input)
        print(f"Agent: {reply}")

if __name__ == "__main__":
    run_chat()