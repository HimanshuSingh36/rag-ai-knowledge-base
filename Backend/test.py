import requests, os
from dotenv import load_dotenv
load_dotenv()

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {os.getenv('openrouter_api_key')}"},
    json={"model": "openrouter/free", "messages": [{"role": "user", "content": "hi"}]}
)
print(response.status_code)
print(response.text)