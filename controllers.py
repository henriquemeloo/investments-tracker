import datetime
import calendar
import json
from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd

#client = MongoClient('mongodb://db:27017/')
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def str_to_date(str_date): #must be in format YYYY-MM-DD
	str_date = str_date.split('-')
	return datetime.date(int(str_date[0]), int(str_date[1]), int(str_date[2]))

def hello():
	return "Hello World!"

def users():
	if request.method == 'GET':
		users = db.users.find()
		return JSONEncoder().encode({"status": "success", "payload": [user for user in users]})
	elif request.method == 'POST':
		try:
			name = request.form["name"]
			user_id = db.users.insert_one({'name': name}).inserted_id
			return JSONEncoder().encode({"status": "success", "payload": str(user_id)})
		except Exception:
			return JSONEncoder().encode({"status": "failed", "payload": "Favor colocar um nome"})

def goals(user_id):
	if request.method == 'GET':
		goals = db.goals.find({ "user_id": user_id })
		return JSONEncoder().encode({"status": "success", "payload": [goal for goal in goals]})
	elif request.method == 'POST':
		try:
			name = request.form["name"]

			for goal in db.goals.find():
				if goal.get("name") == name:
					return JSONEncoder().encode({
						"status": "failed",
						"payload": "Ja existe objetivo de mesmo nome"
						})

			goal_id = db.goals.insert_one({
				'user_id': user_id,
				'name': name,
				'price': float(request.form["price"]),
				'end_date': request.form["end_date"], #must be in format YYYY-MM-DD
				'start_date': request.form["start_date"], #must be in format YYYY-MM-DD
				'ammount_saved': float(request.form["ammount_saved"]),
				'last_paid': request.form["last_paid"] #must be in format YYYY-MM-DD
				}).inserted_id
			return JSONEncoder().encode({"status": "success", "payload": str(goal_id)})

		except Exception:
			return JSONEncoder().encode({"status": "failed", "payload": "Error"})

def goal(user_id, goal_id):
	goal = db.goals.find_one({'_id': ObjectId(goal_id)})
	return JSONEncoder().encode({"status": "success", "payload": goal})


def get_pending_installments(user_id):
	cursor = db.goals.find()
	goals = pd.DataFrame(list(cursor))
	goals['last_paid'] = goals.apply(lambda row : str_to_date(row['last_paid']), axis=1)
	goals['end_date'] = goals.apply(lambda row : str_to_date(row['end_date']), axis=1)
	pending_installments = goals.loc[goals['last_paid'] < datetime.datetime.now().date()].copy()
	if pending_installments.empty:
		return JSONEncoder().encode({"status": "success", "payload": None})
	pending_installments['months_delta'] = pending_installments.apply(lambda row : diff_month(row['end_date'], datetime.datetime.now().date()), axis=1)
	pending_installments['monthly_ammount'] = pending_installments.apply(lambda row : row['price'] / row['months_delta'], axis=1)
	pending_installments['last_paid'] = pending_installments.apply(lambda row : str(row['last_paid']), axis=1)
	pending_installments['end_date'] = pending_installments.apply(lambda row : str(row['end_date']), axis=1)

	return JSONEncoder().encode({"status": "success", "payload": pending_installments.drop(columns=['_id']).to_dict()})

def update_goal(user_id, goal_id, name=None, price=None, end_date=None, ammount_saved=None, last_paid=None):
	update_value = {
		'name': name,
		'price': price,
		'end_date': end_date,
		'ammount_saved': ammount_saved,
		'last_paid': last_paid
		}
	filtered = {k: v for k, v in update_value.items() if v is not None}
	update_value.clear()
	update_value.update(filtered)

	db.goals.update_one(
		filter={'_id':ObjectId(goal_id)},
		update={"$set":update_value},
		upsert=False
		)

	return JSONEncoder().encode({"status": "success", "payload": db.goals.find_one({'_id':ObjectId(goal_id)})})

def pay_ammount(user_id, goal_id):
	ammount = float(request.form["ammount"])
	ammount_saved = float(db.goals.find_one({'_id':ObjectId(goal_id)})['ammount_saved'])
	last_paid = datetime.datetime.now().date().strftime(format="%Y-%m-%d")
	
	return update_goal(user_id, goal_id, ammount_saved=ammount_saved+ammount, last_paid=last_paid)