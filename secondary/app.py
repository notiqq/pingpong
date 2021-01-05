import requests
import sys
import time
from flask import Flask, redirect
from flask import request
from flask import jsonify, make_response
import json
import os as os
import time
from data_access import DataProvider
from models import Message
from helpers import Helper

app = Flask(__name__)


@app.route("/", methods=["GET"])
def save_data():
    delay = int(0 if "DELAY" not in os.environ else os.environ["DELAY"])
    time.sleep(delay)

    text = request.args.get("message")
    uuid = request.args.get("message_id")
    stamp = request.args.get("stamp")

    if text == None or uuid == None or stamp == None:
        return redirect("all", code=303)
    stamp = Helper.decode_base64(stamp)
    message = Message(text, uuid, stamp)
    DataProvider.add_message(message)
    return jsonify(DataProvider.get_messages(), 200)


@app.route("/health-check", methods=["GET"])
def get_health_check_data():
    return ('', 200)

@app.route("/all", methods=["GET"])
def get_saved_data():
    return jsonify(DataProvider.get_messages(), 200)


@app.route("/clear", methods=["GET"])
def clear_data():
    DataProvider.save_messages({})
    return redirect("all", code=303)


if __name__ == "__main__":
    port = 5000 if "PORT" not in os.environ else os.environ["PORT"]
    app.run("0.0.0.0", port, debug=True)
