import requests

url = "http://192.168.1.11:82/upload/luckyNumber.sol"
response = requests.get(url)
print(response.content)
with open("xx.sol", "w", encoding="utf-8") as f:
    f.write(response.content.decode())
    f.close()
    