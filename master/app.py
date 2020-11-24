import requests
import sys
import time
import configs as config
import json
import os as os
from flask import Flask, session, redirect
from flask import request
from flask import jsonify
from flask_session import Session

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


@app.route("/", methods=["POST", "GET"])
def submit_to_secondaries():
    message = None
    if request.method == "POST":
        message = request.form["message"]
    if request.method == "GET":
        message = request.args.get("message")
    if message == None:
        return redirect("all", code=303)
    try:
        try:
            requests.get(f"{config.first_node_url}?message={message}")
        except Exception as ex:
            add_message(str(ex))
        try:
            requests.get(f"{config.second_node_url}?message={message}")
        except Exception as ex:
            add_message(str(ex))
        add_message(message)
    except Exception as ex:
        return (ex, 500)

    return redirect("all", code=303)


@app.route("/all", methods=["GET"])
def get_submitted_data():
    data = get_messages()
    return jsonify(data)


@app.route("/clear", methods=["GET"])
def clear_data():
    save_messages([])
    try:
        requests.get(f"{config.first_node_url}/clear")
    except:
        pass

    try:
        requests.get(f"{config.second_node_url}/clear")
    except:
        pass
    return redirect("all", code=303)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
