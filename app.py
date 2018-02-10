from flask import Flask, request, jsonify
from pymongo import MongoClient

from controllers import index
#, users

app = Flask(__name__)

#client = MongoClient('mongodb://db:27017/')
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database

@app.route("/users", methods=['GET', 'POST'])
def users_route():
    if request.method == 'GET':
        users = []
        for user in db.users.find():
            users.append(user.get("name", ""))
        return jsonify({"status": "success", "payload": users})
    elif request.method == 'POST':
        user_id = db.users.insert_one({'name': 'user name'}).inserted_id
        return jsonify({"status": "success", "payload": str(user_id)})

@app.route("/")
def hello():
    return index()

if __name__ == "__main__":
    app.run(host="localhost", debug=True)
    #app.run(host="0.0.0.0", debug=True)
