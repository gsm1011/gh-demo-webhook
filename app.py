#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import requests

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
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# actions
# display image.
# next image.
# previous image.
# play video.
def processRequest(req):
    '''
    Handling the action requests. The action name should be specified in the
    api.ai platform.
    '''
    action = req.get("result").get("action")
    
    print ('Action:')
    print (action)
    
    what = 'what'
    host = '71.10.207.235'
    port = '8081'
    url = 'http://' + host + ':' + port
    # url = 'https://www.google.com'
    errorMsg = 'Something wrong with the cast controller.'
    # action = 'abc'
    if action == 'displayImage':
        r = requests.get(url + '/displayImage')
        if r.status_code != 200:
            what = errorMsg
        else:
            what = 'displaying the image now. '
            
    elif action == 'nextImage':
        r = requests.get(url + '/nextImage')
        if r.status_code != 200:
            what = errorMsg
        else:
            what = 'displaying next image'
            
    elif action == 'previousImage':
        r = requests.get(url + '/previousImage')
        if r.status_code != 200:
            what = errorMsg
        else:
            what = 'previous image'
            
    elif action == 'playVideo':
        r = requests.get(url + '/playVideo')
        if r.status_code != 200:
            what = errorMsg
        else:
            what = 'playing video.'
    else:
        what = 'what do you want to do'

    res = makeWebhookResult(what)
    return res


def makeWebhookResult(data):

    print("Response:")
    print(data)

    return {
        "speech": data,
        "displayText": data,
        # "data": data,
        # "contextOut": [],
        "source": "google-home-multimedia-demo"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
