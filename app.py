from flask import Flask, request, jsonify
from pymongo import MongoClient

from controllers import *

app = Flask(__name__)

#client = MongoClient('mongodb://db:27017/')
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database

#ROUTES---------------------------------------------------------------------------------------

@app.route("/")
def hello_route():
    return hello()

@app.route("/users", methods=['GET', 'POST'])
def users_route():
    return users()

@app.route("/users/goals", methods=['GET', 'POST'])
def goals_route():
    return goals()


#---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="localhost", debug=True)
    #app.run(host="0.0.0.0", debug=True)
