from flask import Flask, request,jsonify
from flask_cors import cross_origin, CORS

from onerouterequest import main

import json


app = Flask(__name__)
#cors = CORS(app)
#CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/lat=<float:lat>&long=<float:long>',methods=['GET'])
#@cross_origin() # allow all origins all methods

def  method(lat,long):

    x  = main(lat,long)
    #x[0].update(x[1])
    #y = json.dumps(str(x))
   # print(json.loads(y))

    print(len(x))
    return x
@app.route('/json/',methods=['POST'])
def  method1():

    content = request.get_json(silent=True)
    #x  = main(lat,long)
    #x[0].update(x[1])
    #y = json.dumps(str(x))
   # print(json.loads(y))

    #print(len(x))
    print (content)
    return jsonify(request.json)
    
@app.route('/')
def  method1():

   
    #x  = main(lat,long)
    #x[0].update(x[1])
    #y = json.dumps(str(x))
   # print(json.loads(y))

    #print(len(x))
   
    return 'hi'

if __name__ == '__main__':
    app.run()
