import os

master_node_url = (
    "http://localhost:5000" if "PORT" not in os.environ else "http://192.168.32.1:5000"
)