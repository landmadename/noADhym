from pyrogram import Client, filters
import config
import re
from datetime import datetime
from collections import deque
from fuzzywuzzy import fuzz
import time
from pyrogram.handlers import MessageHandler
import _thread

app = Client("+8618615710956")
chat_id = "noADhym"
pool = deque(maxlen=10)

def keywords_check(client, message):
    data = ("" if message.text is None else message.text) + ("" if message.caption is None else message.caption)
    for keyword in config.keywords:
        if re.search(keyword, data) is not None:
            for i in pool:
                if fuzz.ratio(data, i)>60:
                    return False
            pool.append(data)
            client.send_message(chat_id, "关键词："+keyword)
            return True
    return False

def channel_check(client, message):
    if message.sender_chat is None:
        return False
    channel_name = message.sender_chat["username"]
    if channel_name not in config.channel_rules:
        return False
    rules = config.channel_rules[channel_name]
    data = ("" if message.text is None else message.text) + ("" if message.caption is None else message.caption)
    for rule in rules:
        if re.search(rule, data) is not None:
            for i in pool:
                if fuzz.ratio(data, i)>60:
                    return False
            pool.append(data)
            client.send_message(chat_id, "关键词："+rule)
            return True
    return False

# @app.on_message()
def my_handler(client, message):
    print(message.text)
    print(message.caption)
    print(datetime.now())
    print("--------------")
    if keywords_check(client, message) is True:
        message.forward(chat_id)
        return
    if channel_check(client, message) is True:
        message.forward(chat_id)
        return

handler = MessageHandler(my_handler)
app.add_handler(handler)
# _thread.start_new_thread(main,())
app.run()
