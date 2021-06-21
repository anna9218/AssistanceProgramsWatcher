import json
import os
import sys

from flask import Flask, jsonify, request
# TODO: for downloading flask_cors run this line in terminal: conda install -c anaconda flask_cors
from flask_cors import CORS

sys.path.append(os.getcwd().split('\WebCommunication')[0])


app = Flask(__name__)
CORS(app)




if __name__ == '__main__':
    app.run()
