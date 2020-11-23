import requests
import sys
import time
from flask import Flask
from flask import request

from app.msg_list import MsgList

app = Flask(__name__)

msg_list = MsgList()

@app.route('/list_msg')
def list_msg():
    return msg_list.get_mesg()


@app.route('/ping')
def ping(args):
    iteration = int(request.args.get('iteration') or args[0])
    iterations = int(request.args.get('iterations') or args[1])

    iteration += 1
    if iteration <= int(iterations):
        payload = {'iteration': iteration, 'iterations': iterations}
        print(int(round(time.time()*1000)), " ping ", iteration, file = sys.stderr)
        print(int(round(time.time()*1000)), " ping ", iteration, file = sys.stdout)
        r1 = requests.get('http://pong:5001/pong', params = payload)
    return 'fuck', 200

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)