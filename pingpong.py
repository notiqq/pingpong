from flask import Flask
app = Flask(__name__)
@app.route('/ping')
def ping():
    return 'pong', 200

@app.route('/pong')
def pong():
    return 'ping', 200

@app.route('/pingpong')
def pingpong():
    return 'pingpong', 200

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)