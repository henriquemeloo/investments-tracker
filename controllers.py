import datetime
import calendar
import json
from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

#client = MongoClient('mongodb://db:27017/')
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def hello():
	return "Hello World!"

def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day,calendar.monthrange(year,month)[1])
    
    return datetime.date(year, month, day)

#def users():


def goals(user_id):
	if request.method == 'GET':
		goals = db.goals.find({ "user_id": user_id })
		return JSONEncoder().encode({"status": "success", "payload": [goal for goal in goals]})
	elif request.method == 'POST':
		try:
			name = request.form["name"]
			price = request.form["price"]
			end_date = str(request.form["end_date"]) #ESPERADA DATA NO FORMATO MM-YYYY
			month = int(end_date.rpartition('-')[0])
			year = int(end_date.rpartition('-')[2])
			end_date = datetime.date(year, month, 1)
			start_date = str(request.form["start_date"])
			month = int(start_date.rpartition('-')[0])
			year = int(start_date.rpartition('-')[2])
			start_date = datetime.date(year, month, 1)


			for goal in db.goals.find():
				if goal.get("name") == name:
					return JSONEncoder().encode({"status": "failed", "payload": "Ja existe objetivo de mesmo nome"})

			num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
			installments_ids = []
			for i in range(num_months):
				value = float(price)/num_months 
				date = add_months(start_date, i)
				installment_id = db.installments.insert_one({'value': value, 'paid': "False", 'date': str(date), 'investment_id': "None"}).inserted_id
				installments_ids.append(installment_id)

			goal_id = db.goals.insert_one({'user_id': user_id, 'name': name, 'price': price, 'end_date': str(end_date), 'start_date': str(start_date), 'installments': installments_ids}).inserted_id
			return jsonify({"status": "success", "payload": str(goal_id)})

		except Exception as e:
			return jsonify({"status": "failed", "payload": "Error"})

def goal(user_id, goal_id):
	goal = db.goals.find_one({'_id': ObjectId(goal_id)})
	return JSONEncoder().encode({"status": "success", "payload": goal})