import sys
import json
from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
from controllers import *
app = Flask(__name__)

#client = MongoClient('mongodb://db:27017/')
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database

#ROUTES---------------------------------------------------------------------------------------

""" class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o) """

@app.route("/")
def hello_route():
    return hello()

@app.route("/users", methods=['GET', 'POST'])
def users_route():
    if request.method == 'GET':
        users = db.users.find()
        return JSONEncoder().encode({"status": "success", "payload": [user for user in users]})
    elif request.method == 'POST':
        try:
            name = request.form["name"]
            user_id = db.users.insert_one({'name': name}).inserted_id
            return jsonify({"status": "success", "payload": str(user_id)})
        except Exception as e:
            return jsonify({"status": "failed", "payload": "Favor colocar um nome"})

@app.route("/user/<user_id>", methods=['GET'])
def user_route(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    return JSONEncoder().encode({"status": "success", "payload": user})

@app.route("/goals/<user_id>", methods=['GET', 'POST'])
def goals_route(user_id):
    return goals(user_id)

@app.route("/goals/<user_id>/<goal_id>", methods=['GET'])
def goal_route(user_id, goal_id):
    return goal(user_id, goal_id)

"""@app.route("/installments/<installment_id>", methods=['GET'])
def installment_route(installment_id):
    return installment(installment_id)

@app.route("/installments/<installment_id>/pay", methods=['POST'])
def installment_pay_route(installment_id):
    return pay_installment(installment_id)"""

@app.route("/goals/pending/<user_id>/")
def pending_installments_route(user_id):
    return get_pending_installments(user_id)

@app.route("/goals/<user_id>/<goal_id>/pay", methods=['POST'])
def pay_ammount_route(user_id, goal_id):
    return pay_ammount(user_id, goal_id)

#---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="localhost", debug=True)
    #app.run(host="0.0.0.0", debug=True)
