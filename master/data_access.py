import os as os
import json


class DataProvider:

    STORAGE_NAME = "data.json"
    HEALTHY_DATA_STORAGE_NAME = "healthy_data.json"

    @staticmethod
    def get_health_statuses():
        data = []
        if not os.path.exists(DataProvider.HEALTHY_DATA_STORAGE_NAME):
            with open(DataProvider.HEALTHY_DATA_STORAGE_NAME, "w"):
                pass
        with open(DataProvider.HEALTHY_DATA_STORAGE_NAME, "r+") as openfile:
            try:
                data = json.load(openfile)
            except:
                data = []
        return data
        
    @staticmethod
    def save_health_statuses(data):
        with open(DataProvider.STORAGE_NAME, "w") as outfile:
            json.dump(data, outfile)

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
        messages.append(message)
        DataProvider.save_messages(messages)
        return messages
