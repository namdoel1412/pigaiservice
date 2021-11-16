from flask import Flask, json, render_template, request, redirect, url_for
from flask.helpers import make_response
import pymongo
from bson.objectid import ObjectId
from query.behaviour_query import lstBehaviourQueryByPigAIId
from query.event_query import lstEventQueryByFarmId
from query.pen_query import lstPenByFarmId
from util.http import failedResponse, successResponse
from bson import json_util
from query.farm_query import lstFarmQueryByOwnerId
from util.jsonEncoder import JSONEncoder
from flask import jsonify


app = Flask(__name__)
client = pymongo.MongoClient("mongodb://DODINHNAM:27017,DODINHNAM:27018,DODINHNAM:27019")
db = client["pigai"]
events_collection = db["events"]
behaviours_collection = db["behaviours"]
eventtypes_collection = db["eventtypes"]
pens_collection = db["pens"]
pigs_collection = db["pigs"]
weighttypes_collection = db["weighttypes"]
farm_collection = db["farms"]

# FARM - ownerId
@app.route("/farm/ownerId", methods=["POST"])
def getFarmByOwnerId():
	try:	
		req = request.json
		_offset = req['offset']
		_size = req['size']
		_ownerId = req['ownerId']
		tmp = farm_collection.aggregate(lstFarmQueryByOwnerId(_ownerId, _offset, _size))
		c = []
		for i in tmp:
			c.append(i)
		return make_response(successResponse(c))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute getFarmByOwnerId API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api", "Exception"),500)

# FARM - Tạo Farm
@app.route("/farms", methods=["POST"])
def home():
	try:
		req = request.json
		_name = req['name']
		_address = req['address']
		_ownerId = req['ownerId']
		print(_name)
		print(_address)
		print(_ownerId)
		if not _name or not _address or not _ownerId:
			return make_response(failedResponse('IdsRequired', 'IdsRequired'))
		data = {
			"name": _name,
			"address": _address,
			"ownerId":  _ownerId
		}
		farm_collection.insert_one(data)
		data['id'] = str(data['_id'])
		data.pop('_id')
		print(data)
		# for i in result:
		# 	res.append(i)
		return make_response(successResponse(data))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute getFarmByOwnerId API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api", "Exception"),500)

# FARM - Tạo UpdateFarm
@app.route("/farms/<string:farmId>", methods=["PUT"])
def updateFarm(farmId):
	try:
		req = request.json
		_name = req['name']
		_address = req['address']
		_ownerId = req['ownerId']
		if (not _name or not _ownerId):
			return failedResponse('BodyRequired', 'BodyRequired')
		data = {
			"name": _name,
			"address": _address,
			"ownerId":  _ownerId
		}
		event = farm_collection.update_one({ "_id": { "$eq": ObjectId(farmId) } },  { "$set": data })
		# data['id'] = str(data['_id'])
		# data.pop('_id')
		# print(data)
		# for i in result:
		# 	res.append(i)
		return make_response(successResponse(data))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute highlightID API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api calculate highlight ID", "Exception"),500)

@app.route("/farms/<string:farmId>", methods=["DELETE"])
def deleteFarm(farmId):
	try:
		farm_collection.remove({"_id": ObjectId(farmId)})
		return make_response(successResponse(True))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute highlightID API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api calculate highlight ID", "Exception"),500)
	

# BEHAVIOURS
@app.route("/behaviours/pigAIId/<string:pigAIId>", methods=["GET"])
def getBehaviourByPigAIId(pigAIId):
	try:
		res = behaviours_collection.aggregate(lstBehaviourQueryByPigAIId(pigAIId, 0, 10))
		c = []
		for i in res:
			c.append(i)
		return make_response(successResponse(c))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute highlightID API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api calculate highlight ID", "Exception"),500)

# EVENTS
@app.route("/events/farmId/<string:farmId>", methods=["POST"])
def getEventsByFarmId(farmId):
	try:
		if request.json:
			params = request.json
		else:
			params = request.form
		print(params)
		res = events_collection.aggregate(lstEventQueryByFarmId(farmId, params['offset'], params['size']))
		c = []
		for i in res:
			c.append(i)
		return make_response(successResponse(c))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute highlightID API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api calculate highlight ID", "Exception"),500)

# EVENT - Tạo event
@app.route("/events", methods=["POST"])
def createEvent():
	try:
		req = request.json
		# _name = req['name']
		# _address = req['address']
		# _ownerId = req['ownerId']
		# print(_name)
		# print(_address)
		# print(_ownerId)
		print(req)
		events_collection.insert_one(req)
		req['id'] = str(req['_id'])
		req.pop('_id')
		print(req)
		# for i in result:
		# 	res.append(i)
		return make_response(successResponse(req))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute getFarmByOwnerId API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api", "Exception"),500)

# Events - UpdateEvent
@app.route("/events/<string:eventId>", methods=["PUT"])
def updateEvent(eventId):
	try:
		req = request.json
		event = events_collection.update_one({ "_id": { "$eq": ObjectId(eventId) } },  { "$set": req })
		return make_response(successResponse(req))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute highlightID API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api calculate highlight ID", "Exception"),500)

@app.route("/events/<string:eventId>", methods=["DELETE"])
def deleteEvents(eventId):
	try:
		events_collection.remove({"_id": ObjectId(eventId)})
		return make_response(successResponse(True))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute highlightID API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api calculate highlight ID", "Exception"),500)

# --
# PEN
@app.route("/pens/allPen/<string:farmId>", methods=["GET"])
def getPensByFarmId(farmId):
	try:
		_offset = request.args.get('offset')
		_size = request.args.get('size')
		print(_offset)
		print(_size)
		res = pens_collection.aggregate(lstPenByFarmId(farmId, _offset, _size))
		print('success')
		c = []
		for i in res:
			c.append(i)
		return make_response(successResponse(c))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute highlightID API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api calculate highlight ID", "Exception"),500)

# Pen - Tạo pen
@app.route("/pens", methods=["POST"])
def createPen():
	try:
		req = request.json
		print(req)
		pens_collection.insert_one(req)
		req['id'] = str(req['_id'])
		req.pop('_id')
		print(req)
		# for i in result:
		# 	res.append(i)
		return make_response(successResponse(req))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute getFarmByOwnerId API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api", "Exception"),500)

# Pen - Update pen
@app.route("/pens/<string:penId>", methods=["PUT"])
def updatePen(penId):
	try:
		req = request.json
		event = pens_collection.update_one({ "_id": { "$eq": ObjectId(penId) } },  { "$set": req })
		return make_response(successResponse(req))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute highlightID API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api calculate highlight ID", "Exception"),500)

@app.route("/pens/<string:penId>", methods=["DELETE"])
def deletePen(penId):
	try:
		pens_collection.remove({"_id": ObjectId(penId)})
		return make_response(successResponse(True))
	except Exception as e:
		print("Oops!", e.__class__, " error when execute highlightID API")
		print("Next entry.")
		return make_response(failedResponse("Error when execute api calculate highlight ID", "Exception"),500)




@app.route("/fnf/create")
def create():
    return render_template('create.html')


@app.route("/fnf/save", methods=['POST'])
def save():
    name = request.form['name']
    relation = request.form['relation']
    phone = request.form['phone']
    email = request.form['email']

    data = {"name": name, "relation": relation, "phone": phone, "email": email}

    fnf_coll.insert_one(data)
    return redirect(url_for('home'))


@app.route("/fnf/edit/<string:id>")
def edit(id):
    result = fnf_coll.find_one({"_id": ObjectId(id)})
    return render_template('edit.html', member=result)


@app.route("/fnf/update", methods=['POST'])
def update():
    id = request.form['id']
    name = request.form['name']
    relation = request.form['relation']
    phone = request.form['phone']
    email = request.form['email']

    data = {"name": name, "relation": relation, "phone": phone, "email": email}

    fnf_coll.update_one({'_id': ObjectId(id)}, {"$set": data}, upsert=False)
    return redirect(url_for('home'))


@app.route("/fnf/delete/<string:id>", methods=['GET', 'DELETE'])
def delete(id):
    if request.method == 'DELETE':
        if request.json:
            params = request.json
        else:
            params = request.form

        id = params.get('id')

    fnf_coll.remove({"_id": ObjectId(id)})
    return redirect(url_for('home'))
	

if __name__ == "__main__":
    app.run('0.0.0.0', 3001, debug=False, threaded=True, use_reloader=False)