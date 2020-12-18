import requests
import json

url = "http://127.0.0.1:8000/api/uploadSuspect/"

data = { 'name' : "Aslam", "roll": '102'}

json_data = json.dumps(data)

requests.post(url=url, data=json_data)