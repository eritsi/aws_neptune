import os
import json
import pandas as pd
from slack_sdk import WebClient

token_str = "SLACK_API_TOKEN"
client = WebClient(token=token_str)
response = client.users_list()

with open('./users.json','w') as outfile:
    json.dump(response['members'], outfile, indent=4, ensure_ascii=False)

with open('./users.json') as f:
    msgs = json.load(f)
    id = []
    name = []

    for msg in msgs:
        if set(["id", "profile"]) <= msg.keys():
            id.append(msg["id"])
            name.append(msg["profile"]["display_name"])

    test =pd.DataFrame({"name": name, "id": id})

test.to_csv('users.csv')
outfile.close()
os.remove('./users.json')