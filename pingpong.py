import redis
import requests
import sys
import time
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/pingpong')
def pingpong():
    cache.mset({"hits": "0"})
    ping()
    return 'pingpong', 200

@app.route('/ping')
def ping():
    ping_count = cache.incr('hits')
    print ('This is count number ',ping_count, file=sys.stderr)
    if ping_count == 5:
        exit()
    response = requests.get('http://ping:5000/pong').content
    return 'pong', 200

@app.route('/pong')
def pong():
    #response = requests.get('http://pong:5001/ping').content
    return 'ping', 200

def get_ping_count():
    limit = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if limit == 0:
                raise exc
            limit -= 1
            time.sleep(0.5)

#def run_x_times():
#    for i in range (6):
#       print('Iteration number ', i, file=sys.stderr)
#       ping()
    
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)