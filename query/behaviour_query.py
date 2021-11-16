from bson import ObjectId

def lstBehaviourQueryByPigAIId(pigAIId, offset, size):
    objId = ObjectId(pigAIId)
    print(repr(objId))
    return [{
        "$match": {
            "pigAIId": {"$eq": objId}
        },
    },
    {
        "$project": {
            "id": {
                "$toString": '$_id'
            },
            "_id": 0,
            "name": 1,
            "address": 1,
            "owner": '$user'
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