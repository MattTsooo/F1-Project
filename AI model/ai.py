import requests

url = ""
params = {"q": "Monaco", "appid": "b6b414bda24544b3ac5184659250111", "units": "imperial"}
response = requests.get(url, params = params)
data = response.json()
