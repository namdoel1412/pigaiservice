from flask import Flask, json, render_template, request, redirect, url_for
from flask.helpers import make_response
import pymongo
from bson.objectid import ObjectId
from util.http import successResponse
from bson import json_util
from query.farm_query import lstFarmQueryByOwnerId
from util.jsonEncoder import JSONEncoder

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://DODINHNAM:27017")
db = client["pigai"]
events_collection = db["events"]
behaviours_collection = db["behaviours"]
eventtypes_collection = db["eventtypes"]
pens_collection = db["pens"]
pigs_collection = db["pigs"]
weighttypes_collection = db["weighttypes"]
farm_collection = db["farms"]


@app.route("/")
def home():
	tmp = farm_collection.aggregate(lstFarmQueryByOwnerId("614c2a866a84c95e342dfd4f", 0, 10))
	c = []
	for i in tmp:
		c.append(i)
	a = list(tmp)
	print(a)
	b = None
	for i in tmp:
		b = i
	print(b)
	#return make_response(successResponse(JSONEncoder().encode(c)))
	#return make_response(successResponse(json.dumps(c, default=str)))
	return make_response(successResponse(c))
	# docs_list  = list(events_collection.find())
	# return json.dumps(tmp, default=json_util.default)


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