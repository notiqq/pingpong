import requests
import sys
from flask import Flask
app = Flask(__name__)
@app.route('/ping')
def ping():
    #count = get_hit_count()
    response = requests.get('http://ping:5000/pong').content
    print('Hello world!', file=sys.stderr)
    print('This is standard output', file=sys.stderr)
    return 'pong', 200

@app.route('/pong')
def pong():
    #response = requests.get('http://pong:5001/ping').content
    return 'ping', 200

@app.route('/pingpong')
def pingpong():
    run_x_times()
    return 'pingpong', 200

def run_x_times():
    for i in range (6):
        print('Iteration number ', i, file=sys.stderr)
        ping()
    
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)