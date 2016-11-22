#!/usr/bin/env python

import json
import os.path
from random import randint
import random

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/swap')
def hello():
    data = 'The Service Manual is located here: ' + "http://www.rockabilly.net/files/manuals/DVR-520H-service-manual.pdf"
    res = makeWebhookResult(data)
    print("Res:")
    print(res)
    return app.response_class(res, content_type='application/json')

@app.route('/dvr')
def isDvrOn():
    data = "DVR is OFF"
    num = randint(0,9)
    if (num % 2 == 0):
        data = "DVR is OFF"
    else:
        data = "DVR is ON"
    res = makeWebhookResult(data)
    print("Res:")
    print(res)
    return app.response_class(res, content_type='application/json')

@app.route('/downgrade', methods=['POST'])
def test():
    data = 'The Service Manual is located here: ' + "http://www.rockabilly.net/files/manuals/DVR-520H-service-manual.pdf"
    res = makeWebhookResult(data)
    print("Res:")
    print(res)
    return app.response_class(res, content_type='application/json')


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "swapDVR":
        data = 'The Service Manual is located here: ' + "http://www.rockabilly.net/files/manuals/DVR-520H-service-manual.pdf"
        res = makeWebhookResult(data)
        return res
    if req.get("result").get("action") == "downgradeProfile":
        data = index()
        res = makeWebhookResult(data)
        return res
    if req.get("result").get("action") == "checkDVR":
        data = "Hmm...I don't see the DVR Online. We'll have to try another DVR or port. Do you have another DVR you can try"
        num = randint(0,9)
        if (num % 2 == 0):
            data = "Hmm...I don't see the DVR Online. We'll have to try another DVR or port. Do you have another DVR you can try"
        else:
            data = "Looks good. I see the DVR is Online from my side"
        res = makeWebhookResult(data)
        return res

def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))

    speech = data

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "custom web hook"
    }

def index():
    counter = 0
    PATH='./file.txt'
    messages = [
                'Working on Order now',
                "Waiting for the order to flow in BBNS",
                "Still waiting on the flow",
                "Still Waiting",
                "Thank you for waiting, I am working on it"
            ]

    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        print ("File exists and is readable")
        myFile = open(PATH,'r')
        line = myFile.read()
        myFile.close()
        cc = line.strip()
        c = int(cc)
        c += 1
        myFile=open(PATH, 'wt')
        myFile.write(str(c))
        myFile.close()
        
        if c < 5:
            return messages[c]
        else:
            os.remove(PATH)
            order_id = random.randint(100000000000,999999999999)
            return "I have submitted the order successfully. Your Order Number is " + str(order_id)   
           
    else:
        print ("Either file is missing or is not readable")
        
        myFile=open(PATH, 'wt')
        myFile.write(str(counter))
        myFile.close()
        return "Working on it"


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

