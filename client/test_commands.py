import json

with open("client_config.json", "r") as file:
    content = file.read()
    content = json.loads(content)
    print(content["name"])
