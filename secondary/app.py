import requests
import sys
import time
from flask import Flask, redirect
from flask import request
from flask import jsonify, make_response
import json
import os as os
import time

app = Flask(__name__)
STORAGE_NAME = "data.json"


def get_messages():
    data = []
    if not os.path.exists(STORAGE_NAME):
        with open(STORAGE_NAME, "w"):
            pass
    with open(STORAGE_NAME, "r+") as openfile:
        try:
            data = json.load(openfile)
        except:
            data = []
    return data


def save_messages(data):
    with open(STORAGE_NAME, "w") as outfile:
        json.dump(data, outfile)


def add_message(message):
    messages = get_messages()
    messages.append(message)
    save_messages(messages)
    return messages


@app.route("/", methods=["GET"])
def save_data():
    delay = int(0 if "DELAY" not in os.environ else os.environ["DELAY"])
    time.sleep(delay)

    message = request.args.get("message")
    if message == None:
        return redirect("all", code=303)
    add_message(message)
    return jsonify(get_messages(), 200)


@app.route("/all", methods=["GET"])
def get_saved_data():
    return jsonify(get_messages(), 200)


@app.route("/clear", methods=["GET"])
def clear_data():
    save_messages([])
    return redirect("all", code=303)


if __name__ == "__main__":
    port = 5000 if "PORT" not in os.environ else os.environ["PORT"]
    app.run("0.0.0.0", port, debug=True)
