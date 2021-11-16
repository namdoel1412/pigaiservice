from bson import ObjectId
# câu lệnh query lấy list event theo farmId
def lstEventQueryByFarmId(farmId, offset, size):
    objId = ObjectId(farmId)
    print(repr(objId))
    return [{
        "$match": {
            "farmIds": { "$all": [objId]}
        },
    },
    # {
    #     "$lookup": {
    #         "from": "farms",
    #         "let": {["farmIds"]: "$farmIds"},
    #         "as": "farms",
    #         "pipeline": [
    #             {
    #                 "$match": {"$expr": {"$in": ['$_id', "$$farmIds"]}}
    #             },
    #             {
    #                 "$project": {
    #                     "id": {
    #                         "$toString": '$_id'
    #                     },
    #                     "_id": 0,
    #                     "name": 1,
    #                     "address": 1
    #                 }
    #             }
    #         ]
    #     }
    # },
    {
        "$project": {
            "id": {
                "$toString": '$_id'
            },
            "_id": 0,
            "eventType": '$eventType',
            "farms": '$farms',
            "pens": '$pens',
            "pigs": '$pigs',
            "name": 1,
            "desc": 1,
            "startDate": 1,
            "endDate": 1,
            "from": 1,
            "to": 1,
        }
    },
    {
        "$facet": {
            "count": [{"$count": 'total'}],
            "items": [
                {"$skip": +offset},
                {"$limit": +size},
            ],
        },
    },
    {
        "$project": {
            "items": 1,
            "total": {
                "$cond": {
                    "if": {"$eq": [{"$size": '$count'}, 0]},
                    "then": 0,
                    "else": {"$arrayElemAt": ['$count.total', 0]}
                },
            },
        },
    }]

# def lookupObject(collectionName, foreignName, customPipline):
#     return {
#         "$lookup": {
#         "from": collectionName,
#         "let": {[foreignName]: f"${foreignName}"},
#         "as": collectionName,
#         customPipline
#         }
#     }