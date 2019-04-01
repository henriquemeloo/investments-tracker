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


@app.route("/")
def hello_route():
    return hello()

@app.route("/users/", methods=['GET', 'POST'])
def users_route():
    return users()

@app.route("/<user_id>/", methods=['GET'])
def user_route(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    return JSONEncoder().encode({"status": "success", "payload": user})

@app.route("/<user_id>/goals/", methods=['GET', 'POST'])
def goals_route(user_id):
    return goals(user_id)

@app.route("/<user_id>/goals/<goal_id>/", methods=['GET'])
def goal_route(user_id, goal_id):
    return goal(user_id, goal_id)

@app.route("/<user_id>/goals/pending/")
def pending_installments_route(user_id):
    return get_pending_installments(user_id)

@app.route("/<user_id>/goals/<goal_id>/update/", methods=['POST'])
def update_goal_route(user_id, goal_id):
    return update_goal(user_id, goal_id)

@app.route("/<user_id>/goals/<goal_id>/pay/", methods=['POST'])
def pay_ammount_route(user_id, goal_id):
    return pay_ammount(user_id, goal_id)


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
    #app.run(host="0.0.0.0", debug=True)

