import requests
import sys
import time
from flask import Flask
from flask import request
from werkzeug.contrib.cache import SimpleCache
from MSG import MsgList

# msg_list = MsgList()   msg list version doesnt work
app = Flask(__name__)
cache = SimpleCache()  # cache version

@app.route('/', methods=['GET', 'POST'])
def POST_GET_2in1():
    if request.method == "POST":
        try:
            url = request.form['from_Postman']  # Postman message comes here i guess
            msg = requests.get(url)
            cache.set('msg_list', msg)  # adding to the cache
            #msg_list.add_msg(msg)
            print(f'message {msg} was successfully appended to the cache')

            return msg
        except:
            print("Unable to get URL from Postman. Please make sure it's valid and try again.")
    else:
        #output = msg_list.get_msg()
        output = cache.get('msg_list')  # getting out of it
        return output, 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
