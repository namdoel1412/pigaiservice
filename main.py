from flask import Flask, json, render_template, request, redirect, url_for
from flask.helpers import make_response
import pymongo
from bson.objectid import ObjectId
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
	req = request.json
	_offset = req['offset']
	_size = req['size']
	_ownerId = req['ownerId']
	tmp = farm_collection.aggregate(lstFarmQueryByOwnerId(_ownerId, _offset, _size))
	c = []
	for i in tmp:
		c.append(i)
	return make_response(successResponse(c))

# FARM - Tạo Farm
@app.route("/farms", methods=["POST"])
def home():
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

# FARM - Tạo UpdateFarm
@app.route("/farms/<string:farmId>", methods=["PUT"])
def updateFarm(farmId):
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

@app.route("/farms/<string:farmId>", methods=["DELETE"])
def deleteFarm(id):
    if request.method == 'DELETE':
        if request.json:
            params = request.json
        else:
            params = request.form
	id = params.get('id')
	farm_collection.remove({"_id": ObjectId(id)})
	return make_response(successResponse(True))


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