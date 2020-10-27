import requests
import sys
import time
from flask import Flask
from flask import request

app = Flask(__name__)
#cache = redis.Redis(host='redis', port=6379)

@app.route('/pingpong')
def pingpong():
    iterations = request.args.get('iterations')
    start_time = int(round(time.time() * 1000))
    ping(0,iterations)
    end_time = int(round(time.time() * 1000))
    run_time = end_time - start_time
    print (end_time, " Game Over, took ",run_time," ms", file=sys.stderr)
    print (end_time, " Game Over, took ",run_time," ms", file=sys.stdout)
    return 'pingpong', 200

@app.route('/ping')
def ping(*args):
    iteration = int(request.args.get('iteration') or args[0])
    iterations = int(request.args.get('iterations') or args[1])

    iteration += 1
    if iteration <= int(iterations) :
        payload = {'iteration': iteration, 'iterations': iterations}
        print (int(round(time.time() * 1000))," ping ",iteration, file=sys.stderr)
        print (int(round(time.time() * 1000))," ping ",iteration, file=sys.stdout)
        r = requests.get('http://pong:5000/pong', params=payload)
    return 'ping', 200

@app.route('/pong')
def pong(*args):
    iteration = int(request.args.get('iteration') or args[0])
    iterations = int(request.args.get('iterations') or args[1])
    iteration += 1
    if iteration <= int(iterations) :
        payload = {'iteration': iteration, 'iterations': iterations}
        print (int(round(time.time() * 1000))," pong ",iteration, file=sys.stderr)
        print (int(round(time.time() * 1000))," pong ",iteration, file=sys.stdout)
        r = requests.get('http://ping:5000/ping', params=payload)
    return 'pong', 200
    
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)