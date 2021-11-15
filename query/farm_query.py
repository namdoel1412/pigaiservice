from bson import ObjectId
# câu lệnh query lấy list farm theo ownerId
def lstFarmQueryByOwnerId(ownerId, offset, size):
    objId = ObjectId(ownerId)
    print(repr(objId))
    return [{
        "$match": {
            "ownerId": {"$eq": objId}
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