
GATEWAY_URL="http://192.168.2.210:80"
LLM_MODEL="llama3:latest"

curl -H "Content-Type: application/json" \
    -d '{
        "model": "llama2:uncensored",
        "messages": [
            {
                "role": "system",
                "content": "Hi."
            }
        ]
    }' \
    $GATEWAY_URL/v1/chat/completions