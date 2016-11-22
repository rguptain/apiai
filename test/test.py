#!/usr/bin/env python

import json
import os.path

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

def index():
    counter = 0
    PATH='./file.txt'

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
            return "Working on it"
        else:
            os.remove(PATH)
            return "Your Order Number is 123456"   
           
    else:
        print ("Either file is missing or is not readable")
        
        myFile=open(PATH, 'wt')
        myFile.write(str(counter))
        myFile.close()
        return "Working on it"

def processRequest(req):
    if req.get("result").get("action") == "swapDVR":
        data = 'The Service Manual is located here: ' + "http://www.rockabilly.net/files/manuals/DVR-520H-service-manual.pdf"
        res = makeWebhookResult(data)
        return res
    if req.get("result").get("action") == "downgradeProfile":
        data = index()
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


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
