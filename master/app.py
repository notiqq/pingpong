import requests
import sys
import time
import configs as config


import asyncio
import aiohttp
import uuid as uuid

from flask import Flask, session, redirect
from flask import request
from flask import jsonify
from flask_session import Session
from datetime import datetime
from multiprocessing import Process, Value

from data_access import DataProvider
from helpers import Helper
from models import Node, NodeStatus


app = Flask(__name__)


@app.route("/all", methods=["GET"])
def get_submitted_data():
    data = DataProvider.get_messages()
    return jsonify(data)


@app.route("/clear", methods=["GET"])
def clear_data():
    DataProvider.save_messages([])
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
        retry_period_step = 10
        current_retry_period = 10
        max_retry_period = 30
        message_id = str(uuid.uuid4())
        stamp = Helper.encode_base64(datetime.utcnow())
        url = f"{host}?message={message}&message_id={message_id}&stamp={stamp}"
        while True:
            try:
                async with session.get(url) as response:
                    print("Read {0} from {1}".format(response.content_length, url))
                return
            except Exception as ex:
                print(ex)
                print("Reattempting...")
                await asyncio.sleep(current_retry_period)
                if current_retry_period < max_retry_period:
                    current_retry_period += retry_period_step

    async def process_requests(w, message, nodes):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for node in nodes:
                if node.status != NodeStatus.Healthy:
                    continue
                tasks.append(
                        asyncio.ensure_future(
                            make_request(session, node.url, message)
                        )
                    )
            await asyncio.gather(*tasks, return_exceptions=True)

    message = None
    timeout = 30
    w = 0
    if request.method == "POST":
        message = request.form["message"]
        w = int(request.form["w"] if request.form["w"] != None else 0)
    if request.method == "GET":
        message = request.args.get("message")
        w = int(request.args.get("w") if request.args.get("w") != None else 0)
    if message == None:
        return redirect("all", code=303)

    nodes = DataProvider.get_health_statuses()
    nodes_counter = 0
    for node in nodes:
        if node.status == NodeStatus.Healthy:
            nodes_counter += 1
    if nodes_counter == 0:
        return redirect("all", code=303)

    DataProvider.add_message(message)

    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(asyncio.wait_for(process_requests(w, message, nodes),timeout))

    return jsonify({"status": f"Processed {message}"})

def health_check():
    check_period= 10
    node_urls = [config.first_node_url, config.second_node_url]
    nodes = DataProvider.get_health_statuses()
    if len(nodes) == 0:
        nodes = []
        for node_url in node_urls:
            node = Node(node_url, NodeStatus.NotDefined)
            nodes.append(node)

    while True:
        for node in nodes:
            try:
                requests.get(node.url + "/health-check")
                node.status = NodeStatus.Healthy
            except:
                if node.status == NodeStatus.Healthy:
                    node.status = NodeStatus.Suspected
                elif node.status == NodeStatus.NotDefined:
                    node.status = NodeStatus.Unhealthy
                elif node.status == NodeStatus.Suspected:
                    node.status = NodeStatus.Unhealthy
                print(node.url, " ------ ", str(node.status))
            
        DataProvider.save_health_statuses(nodes)
        time.sleep(check_period)
      

if __name__ == "__main__":
    recording_on = Value('b', True)
    background_process = Process(target=health_check, args=(recording_on,))
    background_process.start()  
    app.run(debug=True, host="0.0.0.0", use_reloader=False)
    background_process.join()
    
