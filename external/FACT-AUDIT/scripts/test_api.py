import os, requests, json

api_key = os.getenv('OPENAI_API_KEY', 'NOT_SET')
api_url = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1/chat/completions')

print(f"URL: {api_url}")
print(f"Key: {api_key[:8]}...")

resp = requests.post(api_url,
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    data=json.dumps({"model": "gpt-4o-mini-2024-07-18", "messages": [{"role": "user", "content": "Say hi"}]})
)

print(f"Status: {resp.status_code}")
print(f"Response: {resp.json()}")
