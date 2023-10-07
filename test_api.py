# A simple function to calculate the square of a number 
# the number to be squared is sent in the URL when we use GET 
# on the terminal type: curl http://127.0.0.1:5000 / home / 10 
# this returns 100 (square of 10) 

from flask import Blueprint, jsonify, request

test_blueprint = Blueprint('test_blueprint', __name__)

@test_blueprint.route('/hello', methods = ['GET', 'POST']) 
def home(): 
    if (request.method == 'GET'):
        data = "hello world"
        return jsonify({'data': data})

@test_blueprint.route('/square/<int:num>', methods = ['GET']) 
def disp(num): 
    return jsonify({'data': num**2})
