from enum import Enum

class NodeStatus(Enum):
    NotDefined = 0,
    Healthy = 1,
    Suspected = 2,
    Unhealthy = 3

class Node:
    def __init__(self, url, status):
        self.url = url
        self.status = status