#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os.path
from random import randint
import random

from flask import Flask, send_from_directory
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__, static_url_path='')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/technician')
def checkAgent():
    d = {'rg123q':'Ron Howard', 'vs098t':'Vladimir Putin', 'dd567p':'Dilip Kumar', 'vc345w': 'Vasim S Akram', 'dp345e':'Divya Rana'}
    agent_id = request.args.get('tech-id')
    if agent_id is None:
        return None

    return d[agent_id]

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

def getAgentName(req):
    d = {'rg123q':'Ron Howard', 'vs098t':'Vladimir Putin', 'dd567p':'Dilip Kumar', 'vc345w': 'Vasim S Akram', 'dp345e':'Divya Rana'}
    result = req.get("result")
    parameters = result.get("parameters")
    agent_id = parameters.get("tech-id")
    if agent_id is None:
        return None

    return d[agent_id]

def getSMEName(req):
    d = {'rg123q':'Ron Howard', 'vs098t':'Vladimir Putin', 'dd567p':'Dilip Kumar', 'vc345w': 'Vasim S Akram', 'dp345e':'Divya Rana'}
    result = req.get("result")
    parameters = result.get("parameters")
    sme_id = parameters.get("sme-id")
    if sme_id is None:
        return None

    return d[sme_id]

def processRequest(req):
    if req.get("result").get("action") == "getAgentName":
        data = getAgentName(req)
        res = makeWebhookResult(data)
        return res
    if req.get("result").get("action") == "getSMEName":
       data = getSMEName(req)
       res = makeWebhookResult(data)
       return res
    if req.get("result").get("action") == "swapDVR":
        data = 'The Service Manual is located here: ' + "http://www.rockabilly.net/files/manuals/DVR-520H-service-manual.pdf"
        res = makeWebhookResult(data)
        return res
    if req.get("result").get("action") == "checkCBR":
        data = 'Sure, I can help with that, One moment while I retrieve that information for you. Can you confirm your CBR is 214972xxxx ?'
        res = makeWebhookResult(data)
        return res
    if req.get("result").get("action") == "confirmBANandName":
        data = 'Thanks for verifying the Customer name and the BAN. How can I help you today ?'
        res = makeWebhookResult(data)
        return res
    if req.get("result").get("action") == "submitOMS":
        data = 'Order 2xxxxxx6A was successfully submitted'
        res = makeWebhookResult(data)
        return res
    if req.get("result").get("action") == "submitBBNMS":
        data = 'Order completed successfully through BBNMS,  LPA shows we are on the new profile now.'
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
         "data": {"$FirstName": "Ron", "$MIddleName":"W", "$LastName":"Howard"},
        "contextOut": [{"name":"technician", "lifespan":2, "parameters":{"tech-id":"rg123q", "tech-name":"Ron Howard"}}],
        "speech": speech,
        "displayText": "F",
 
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

