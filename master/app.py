import requests
import sys
import time
import configs as config
import json
import os as os
import asyncio
import aiohttp

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


@app.route("/", methods=["POST", "GET"])
def submit_to_secondaries():
    async def make_request(session, host, message):
        url = f"{host}?message={message}"
        async with session.get(url) as response:
            print("Read {0} from {1}".format(response.content_length, url))

    async def process_requests(w, message):
        async with aiohttp.ClientSession() as session:
            tasks = []
            while w > 0:
                if w % 2 == 0:
                    tasks.append(
                        asyncio.ensure_future(
                            make_request(session, config.first_node_url, message)
                        )
                    )
                else:
                    tasks.append(
                        asyncio.ensure_future(
                            make_request(session, config.second_node_url, message)
                        )
                    )
                w = w - 1
            await asyncio.gather(*tasks, return_exceptions=True)

    message = None
    w = 0
    if request.method == "POST":
        message = request.form["message"]
        w = int(request.form["w"] if request.form["w"] != None else 0)
    if request.method == "GET":
        message = request.args.get("message")
        w = int(request.args.get("w") if request.args.get("w") != None else 0)
    if message == None:
        return redirect("all", code=303)

    add_message(message)

    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(process_requests(w, message))

    return jsonify({"status": f"Processed {message}"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
