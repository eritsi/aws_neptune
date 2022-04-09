import pandas as pd
import json

with open('temp.json') as f:
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

    test =pd.DataFrame({"post_id": ts,"from_user": from_users, "to_user":to_users, "text":list(texts), "root_ts": thread_ts})

print(test)
