import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.post(BASE + "bocuk", json={"text": "oz"})
# response = requests.get(BASE + "bocuk/2dcb56dcf9ccfce02857f07a3c326745")
response = requests.get(BASE + "bocuk")
print(response.json())