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
#    response = requests.get('http://pong:5001/pong').content
#    return response, 200
    ping(0,iterations)
    return 'pingpong', 200

@app.route('/ping')
def ping(*args):
    iteration = int(request.args.get('iteration') or args[0])
    iterations = int(request.args.get('iterations') or args[1])

    iteration += 1
    if iteration <= int(iterations) :
        print ('iteration <- iterations', file=sys.stderr)
        payload = {'iteration': iteration, 'iterations': iterations}
        r = requests.get('http://pong:5000/pong', params=payload)
        print(r.content, file=sys.stderr)
        print ('iteration=',iteration, file=sys.stderr)
        print ('iterations=',iterations, file=sys.stderr)
    #exit()
    return 'pong', 200

@app.route('/pong')
def pong(*args):
    iteration = int(request.args.get('iteration') or args[0])
    iterations = int(request.args.get('iterations') or args[1])
    iteration += 1
    if iteration <= int(iterations) :
        print ('iteration <- iterations', file=sys.stderr)
        payload = {'iteration': iteration, 'iterations': iterations}
        r = requests.get('http://pong:5000/pong', params=payload)
        print(r.content, file=sys.stderr)
        print ('iteration=',iteration, file=sys.stderr)
        print ('iterations=',iterations, file=sys.stderr)
#    response = requests.get('http://ping:5000/pong').content
    return 'ping', 200
    
def finalize():
    print ('Exiting', file=sys.stderr)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)