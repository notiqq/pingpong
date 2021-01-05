import os

base_url = ("http://localhost" if "PORT" not in os.environ else "http://192.168.32.1")

master_node_url = (
    "http://localhost:5000" if "PORT" not in os.environ else "http://192.168.32.1:5000"
)