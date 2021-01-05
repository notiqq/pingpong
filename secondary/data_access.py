import os as os
import json
from marshmallow import Schema, fields

class MessageSchema(Schema):
    message = fields.Str()
    uuid = fields.Str()
    stamp = fields.DateTime()


#TODO serialization to json via marshmallow
class DataProvider:

    STORAGE_NAME = "data.json"

    @staticmethod
    def get_messages():
        data = {}
        if not os.path.exists(DataProvider.STORAGE_NAME):
            with open(DataProvider.STORAGE_NAME, "w"):
                pass
        with open(DataProvider.STORAGE_NAME, "r+") as openfile:
            try:
                data = json.load(openfile)
            except:
                data = {}
        return data

    @staticmethod
    def save_messages(data):
        with open(DataProvider.STORAGE_NAME, "w") as outfile:
            json.dump(data, outfile)

    @staticmethod
    def add_message(message):
        messages = DataProvider.get_messages()
        if message.uuid in messages:
            old_message = messages[message.uuid]
            if old_message.stamp > message.stamp:
                messages[message.uuid] = message

        DataProvider.save_messages(messages)
        return messages
