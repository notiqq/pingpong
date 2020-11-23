import requests
import sys
import time
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/pong')
def pong(*args):
    iteration = int(request.args.get('iteration') or args[0])
    iterations = int(request.args.get('iterations') or args[1])
    iteration += 1
    if iteration <= int(iterations):
        payload = {'iteration': iteration, 'iterations': iterations }
        print(int(round(time.time()*1000)), " pong ", iteration, file = sys.stderr)
        print(int(round(time.time()*1000)), " pong ", iteration, file = sys.stdout)
        r1 = requests.get('http://ping:5000/ping', params = payload)
    return 'pong', 200


if __name__ == '__main__':
    app.run('0.0.0.0', debug = True)