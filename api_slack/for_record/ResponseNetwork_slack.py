import os
import json
import pandas as pd
from slack_sdk import WebClient

# slack APIの設定
token_str = "SLACK_API_TOKEN"
client = WebClient(token=token_str)

# 指定のチャンネルで最新1000件のメインスレ履歴を取得。res.json に結果を書き出す（開発・デバッグ目的）
response = client.conversations_history(channel="SLACK_CHANNEL_CODE", limit=1000)

with open('./res.json','w') as outfile:
    json.dump(response['messages'], outfile, indent=4, ensure_ascii=False)

with open('./res.json') as f:
    msgs = json.load(f)
    texts = []
    ts =[]
    thread_ts = []
    from_users = []
    to_users = []

    for msg in msgs:
        if set(["text", "ts", "thread_ts", "root"]) <= msg.keys():
            ts.append(msg["ts"])
            from_users.append(msg["user"])
            thread_ts.append(msg["thread_ts"])
            to_users.append(msg["root"]["user"])
            texts.append(msg["text"])

    temp =pd.DataFrame({"post_id": ts,"from_user": from_users, "to_user":to_users, "text":list(texts), "root_ts": thread_ts})

# メインスレの投稿のうち、レスがついている投稿について replies投稿を全て取得。 replies.json に結果を書き出す（開発・デバッグ目的）
rep = []
with open('./replies.json','w') as outfile:
    for thread_ts in temp.root_ts.drop_duplicates():
        replies = client.conversations_replies(channel="SLACK_CHANNEL_CODE", limit=1000, ts = thread_ts)
        rep += replies['messages']
    json.dump(rep, outfile, indent=4, ensure_ascii=False)

# 誰(複数)から誰への返答かわかるように表形式にして出力。　親投稿の中身も出力しておく。
with open('./replies.json') as f:
    msgs = json.load(f)
    texts = []
    ts =[]
    thread_ts = []
    from_users = []
    to_users = []

    for msg in msgs:
        if set(["text", "ts", "thread_ts", "reply_users"]) <= msg.keys():
            ts.append(msg["ts"])
            to_users.append(msg["user"])
            thread_ts.append(msg["thread_ts"])
            from_users.append(msg["reply_users"])
            texts.append(msg["text"])

    test =pd.DataFrame({"post_id": ts,"from_user": from_users, "to_user":to_users, "root_text":list(texts), "root_ts": thread_ts})
test.to_csv('output.csv')
f.close()
outfile.close()
# os.remove('./res.json')
# os.remove('./replies.json')