import requests

url = 'http://localhost:8000/tasks/1'
data = [{"task": "My task", "status": True}]

response = requests.get(url)

print(f"Status code: {response.status_code}")
print(f"Response text: {response.text}")
print(response)