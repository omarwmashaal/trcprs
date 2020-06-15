from flask import Flask, request,jsonify
from flask_cors import cross_origin, CORS

from onerouterequest import main

import json


app = Flask(__name__)
#cors = CORS(app)
#NCORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/omar')
#@cross_origin() # allow all origins all methods

def  method():

    return 'omara'

@app.route('/wael',methods=['GET'])
#@cross_origin() # allow all origins all methods

def  method():

    return 'waely'
if __name__ == '__main__':
    app.run()
