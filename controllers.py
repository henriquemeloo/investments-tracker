import datetime
import calendar


def hello():
	return "Hello World!"

def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day,calendar.monthrange(year,month)[1])
    
    return datetime.date(year, month, day)

#def users():


def goals():
	if request.method == 'GET':
		goals = []
		for goal in db.goals.find():
			goals.append(goal.get("name", ""))#COMO INCLUIR TODOS OS DADOS DE CADA GOAL, EM ESPECIAL AS PARCELAS (LISTA)
		return jsonify({"status": "success", "payload": ""})#????????
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
					return jsonify({"status": "failed", "payload": "Ja existe objetivo de mesmo nome"})

			num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
			installments_ids = []
			for i in range(num_months):
				value = price/num_months 
				date = add_months(start_date, i)
				installment_id = db.installments.insert_one({'value': value, 'paid': "False", 'date': date, 'investment_id': "None"})
				installments_ids.append(installment_id)

			goal_id = db.goals.insert_one({'name': name, 'price': price, 'end_date': end_date, 'start_date': start_date, 'installments': installments_ids}).inserted_id
			return jsonify({"status": "success", "payload": str(goal_id)})

		except Exception as e:
			return jsonify({"status": "failed", "payload": "Error"})
