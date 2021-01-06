import os as os
import json
from marshmallow import Schema, fields
from datetime import datetime

class DataProvider:

    app_id = ""
    path = os.path.dirname(os.path.abspath(__file__))
    MESSAGE_STORAGE_PATH = f"{path}/{app_id}data.json"

    @staticmethod
    def set_app_id(app_id):
        DataProvider.MESSAGE_STORAGE_PATH = f"{DataProvider.path}/{app_id}data.json"

    @staticmethod
    def delete_messages_file():
        if os.path.exists(DataProvider.MESSAGE_STORAGE_PATH):
            os.remove(DataProvider.MESSAGE_STORAGE_PATH)

    @staticmethod
    def get_messages():
        data = []
        if not os.path.exists(DataProvider.MESSAGE_STORAGE_PATH):
            with open(DataProvider.MESSAGE_STORAGE_PATH, "w"):
                pass
        with open(DataProvider.MESSAGE_STORAGE_PATH, "r+") as openfile:
            try:
                data = json.load(openfile)
            except:
                data = []
        return data

    @staticmethod
    def save_messages(data):
        with open(DataProvider.MESSAGE_STORAGE_PATH, "w") as outfile:
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
