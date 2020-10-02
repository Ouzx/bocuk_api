import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.post(BASE + "bocuk", json={"text": "oz"}) # post test
# response = requests.get(BASE + "bocuk/2dcb56dcf9ccfce02857f07a3c326745") # get bocuk by token
# response = requests.get(BASE + "bocuk") # get bocuks

# response = requests.post(BASE + "query", json={ # post linkj
#                                                 "link": "bulurum.com",
#                                                 "level": "4",
#                                                 "token": "2dcb56dcf9ccfce02857f07a3c326745"
#                                                 })
response = requests.get(BASE + "query") # get query

print(response.json())