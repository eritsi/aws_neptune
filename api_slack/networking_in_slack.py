import os
import json
import pandas as pd
from slack_sdk import WebClient
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network


# slack APIの設定
token_str = "SLACK_API_TOKEN"
channel_id = "SLACK_CHANNEL_CODE"
client = WebClient(token=token_str)

# 指定のチャンネルで最新1000件のメインスレ履歴を取得。
def get_posts_with_replies(client, channel):
    response = client.conversations_history(channel=channel, limit=1000)

    msgs = response['messages']
    texts = []
    ts =[]
    from_users = []
    to_users = []

    for msg in msgs:
        if set(["text", "ts", "reply_users"]) <= msg.keys():
            for reply_user in msg["reply_users"]:
                ts.append(msg["ts"])
                to_users.append(msg["user"])
                from_users.append(reply_user)
                texts.append(msg["text"])

    posts = pd.DataFrame({"post_ts": ts,"parent_user": to_users, "reply_user":from_users, "text":list(texts)})
    return posts

# ユーザーリスト取得。
def get_user_lists(client):
    user_response = client.users_list()

    msgs = user_response['members']
    id = []
    name = []

    for msg in msgs:
        if set(["id", "profile"]) <= msg.keys():
            id.append(msg["id"])
            name.append(msg["profile"]["real_name"]) # display_name for japanese

    users = pd.DataFrame({"name": name, "id": id})
    return users

# networkx
def plot_nx(posts):
    test = posts.groupby(['parent_user_name', 'reply_user_name'],as_index=False).size().rename(columns={'size':'value'})

    fig = plt.figure(figsize=(24,10))
    G = nx.Graph()
    G.add_nodes_from(posts.parent_user_name.drop_duplicates().to_list())
    # G.add_edges_from([("k", "a", {"weight": 15}), ("n", "a", {"weight": 10}), ("k", "n", {"weight": 5})])
    # 'size'は'weight'ではなく'value'と命名しないと pyvis で太くならない
    G = nx.from_pandas_edgelist(test, "parent_user_name", "reply_user_name", ["value"], create_using=nx.DiGraph())

    options = {
        "font_size": 15,
        "node_size": 500,
        "node_color": "c",
        "edgecolors": "black",
    }

    pos = nx.spring_layout(G)
    # pos = nx.circular_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    # some other layouts 
    # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.kamada_kawai_layout.html
    edge_width = [d["value"] for (u, v, d) in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, width=edge_width)
    nx.draw_networkx(G, pos, **options)

    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()

    pyvis_G = Network()
    pyvis_G.from_nx(G)
    # pyvis_G.enable_physics(True)  #html上でレイアウト動かしたくない場合false
    pyvis_G.show_buttons(filter_=['physics', 'nodes', 'edges'])
    # pyvis_G.set_options("""
    # var options = {
    #   "edges": {
    #     "selfReferenceSize": 0,
    #     "smooth": false
    #   }
    # }
    # """)
    pyvis_G.show("mygraph.html")
    
posts = get_posts_with_replies(client, channel_id)
users = get_user_lists(client)
posts = pd.merge(posts, users.rename(columns={"id":"parent_user", "name":"parent_user_name"})).drop(columns="parent_user")
posts = pd.merge(posts, users.rename(columns={"id":"reply_user", "name":"reply_user_name"})).drop(columns="reply_user")
posts = posts.sort_values('post_ts', ascending=False).reset_index()

display(posts)
posts.to_csv('output.csv')

conversation_counts = posts.groupby(['parent_user_name', 'reply_user_name'],as_index=False).size()
display(conversation_counts)
conversation_counts.to_csv('conversation_counts.csv')

plot_nx(posts)
