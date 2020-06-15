from flask import Flask, request,jsonify
from flask_cors import cross_origin, CORS



import json


app = Flask(__name__)
#cors = CORS(app)
#CORS(app, resources={r"/*": {"origins": "*"}})

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
