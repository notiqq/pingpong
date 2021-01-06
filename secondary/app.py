import requests
import sys
import time
from flask import Flask, redirect
from flask import request
from flask import jsonify, make_response
import json
import os as os
import time

from datetime import datetime
from data_access import DataProvider
from helpers import Helper
from configs import master_node_url, base_url


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
    message = dict(text = text, uuid= uuid, stamp = stamp)
    DataProvider.add_message(message)
    return jsonify(DataProvider.get_messages(), 200)


@app.route("/health-check", methods=["GET"])
def get_health_check_data():
    return ('', 200)

@app.route("/all", methods=["GET"])
def get_saved_data():
    data = DataProvider.get_messages()
    sorted_data = sorted(data,key=lambda x: x.stamp, reverse=True)
    return jsonify(sorted_data, 200)


@app.route("/clear", methods=["GET"])
def clear_data():
    DataProvider.save_messages({})
    return redirect("all", code=303)



def notify_master(port):
    requests.get(master_node_url + f"/notify?port={port}")

def try_port(port):
    result = False
    try:
        url = f"{base_url}:{port}"
        requests.get(url)
        print(f"{port} port is in use")
    except:
        result = True
    return result

if __name__ == "__main__":
    init_port = 5000
    if "PORT" not in os.environ:
        port_found = False
        while port_found == False:
            init_port += 1
            result = try_port(init_port)
            if result != True:
                continue
            break

        app.run(debug=True, host="0.0.0.0", port=init_port, use_reloader=False)
    else:
        port = os.environ["PORT"]
        app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
    
    try:
        notify_master(init_port)
    except:
        pass

    
