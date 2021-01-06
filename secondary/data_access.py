import os as os
import json
from marshmallow import Schema, fields
from datetime import datetime

class DataProvider:

    STORAGE_NAME = "data.json"

    @staticmethod
    def get_messages():
        data = []
        if not os.path.exists(DataProvider.STORAGE_NAME):
            with open(DataProvider.STORAGE_NAME, "w"):
                pass
        with open(DataProvider.STORAGE_NAME, "r+") as openfile:
            try:
                data = json.load(openfile)
            except:
                data = []
        return data

    @staticmethod
    def save_messages(data):
        with open(DataProvider.STORAGE_NAME, "w") as outfile:
            json.dump(data, outfile)

    @staticmethod
    def add_message(message):
        messages = DataProvider.get_messages()
        if any(item['uuid'] == message['uuid'] for item in messages):
            for index in range(len(messages)):
                if messages[index]['uuid'] != message['uuid']:
                    continue
                if datetime(messages[index]['stamp']) > datetime(message['stamp']):
                    messages[index]['stamp'] = message['stamp']
        else:
            messages.append(message)

        DataProvider.save_messages(messages)
        return messages
