#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os.path
from random import randint
import random
from pprint import pprint
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    
    print("Response:")
    print(res)
    
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    
    return r

def processRequest(req):
    if req.get("result").get("action") == "getAgentName":
        data = getAgentName(req)
        ctx = createContext(req, data)
        res = makeWebhookResult(data, ctx)
       
        return res
    
def createContext(req, data):
    input_data = req.get("result").get("contexts")
    context_name = str(input_data[0]["name"])
    context_lifespan = str(input_data[0]["lifespan"])

    return {"name":context_name, "lifespan":context_lifespan, "parameters":{"tech-name":data}},

def makeWebhookResult(data, ctx):
    result = {}
    
    result['speech'] = data
    result['displayText'] = data
    result['data'] = data
    result['contextOut'] = ctx
    result['source'] = "Custom Web Hook"
    
    return result

def getAgentName(req):
    d = {'rg123q':'Ron Howard', 'vs098t':'Vladimir Putin', 'dd567p':'Dilip Kumar', 'vc345w': 'Vasim S Akram', 'dp345e':'Divya Rana'}
    result = req.get("result")
    parameters = result.get("parameters")
    agent_id = parameters.get("tech-id")
    if agent_id is None:
        return None

    return d[agent_id]

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

