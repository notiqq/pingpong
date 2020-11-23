import requests
import sys
import time
from flask import Flask
from flask import request
from flask import jsonify, make_response

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def respond():
    d = requests.get('http://localhost:5000')
    if d:
        return make_response(jsonify(d), 200)

@app.route('/', methods = ['GET'])
def GET(*args):
    r = requests.get('http://localhost:5000')
    print(r)
    return 'request returned', 200


if __name__ == '__main__':
    app.run('0.0.0.0', debug = True)