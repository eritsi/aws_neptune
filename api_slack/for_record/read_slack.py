import json
from slack_sdk import WebClient

token_str = "SLACK_API_TOKEN"
client = WebClient(token=token_str)
response = client.conversations_history(channel="SLACK_CHANNEL_CODE", limit=1000)

with open('./temp.json','w') as outfile:
    json.dump(response['messages'], outfile, indent=4, ensure_ascii=False)

replies = client.conversations_replies(channel="SLACK_CHANNEL_CODE", limit=1000, ts = "1642382967.028900")

with open('./replies.json','w') as outfile:
    json.dump(replies['messages'], outfile, indent=4, ensure_ascii=False)