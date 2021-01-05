import os

base_url = ("http://localhost" if "PORT" not in os.environ else "http://192.168.32.1")

first_node_url = (
    "http://localhost:5001" if "PORT" not in os.environ else "http://192.168.32.1:5001"
)
second_node_url = (
    "http://localhost:5002" if "PORT" not in os.environ else "http://192.168.32.1:5002"
)
