from bson import ObjectId
# câu lệnh query lấy list farm theo ownerId
# def lstPenByFarmId(farmId, offset, size):
#     objId = ObjectId(farmId)
#     print(repr(objId))
#     return [
#         {
#             "$match": {
#                 "farmId": { "$eq": objId }
#             },
#         },
#         # {
#         #     "$lookup": {
#         #         "from": 'weighttypes',
#         #         "let": { "weightTypeId": '$weightTypeId' },
#         #         "pipeline": [
#         #             {
#         #                 "$match": { "$expr": { "$eq": [ '$_id', '$$weightTypeId' ] } }
#         #             },
#         #             {
#         #                 "$project": {
#         #                     "id": {
#         #                         "$toString": '$_id'
#         #                     },
#         #                     "_id": 0,
#         #                     "name": 1,
#         #                 }
#         #             }
#         #         ],
#         #         "as": 'weightType'
#         #     }
#         # },
#         # { 
#         #     #$unwind: '$weightType' 
#         #     "$unwind": {
#         #         "path": '$weightType',
#         #         "preserveNullAndEmptyArrays": True 
#         #     }
#         # },
#         # {
#         #     "$group": {
#         #         "_id": '$_id',
#         #         "id": { "$first": '$_id' },
#         #         "name": { "$first": '$name' },
#         #         "area": { "$first": '$area' },
#         #         "capacity": { "$first": '$capacity' },
#         #         "weightType": { "$first": '$weightType' },
#         #         "note": { "$first": '$note' },
#         #     }
#         # },
#         {
#             "$project": {
#                 "id": {
#                     "$toString": '$_id'
#                 },
#                 "_id": 0,
#                 "name": 1,
#                 "area": 1,
#                 "capacity": 1,
#                 "weightType": 1,
#                 "note": 1,
#             }
#         },
#         {
#             "$facet": {
#                 "count": [ { "$count": 'total' } ],
#                 "items": [
#                     { "$skip": +offset },
#                     { "$limit": +size },
#                 ],
#             },
#         },
#         {
#             "$project": {
#                 "items": 1,
#                 "total": {
#                     "$cond": {
#                         "if": { "$eq": [ { "$size": '$count' }, 0 ] },
#                         "then": 0,
#                         "else": { "$arrayElemAt": [ '$count.total', 0 ] }
#                     },
#                 },
#             },
#         }]

def lstPenByFarmId(farmId, offset, size):
    objId = ObjectId(farmId)
    print(repr(objId))
    return [{
        "$match": {
            "farmId": {"$eq": objId}
        },
    },
    {
        "$project": {
            "id": {
                "$toString": '$_id'
            },
            "_id": 0,
            "name": 1,
            "area": 1,
            "capacity": 1,
            "weightType": 1,
            "note": 1,
        }
    },
    # {
    #     "$facet": {
    #         "count": [{"$count": 'total'}],
    #         "items": [
    #             {"$skip": +offset},
    #             {"$limit": +size},
    #         ],
    #     },
    # },
    # {
    #     "$project": {
    #         "items": 1,
    #         "total": {
    #             "$cond": {
    #                 "if": {"$eq": [{"$size": '$count'}, 0]},
    #                 "then": 0,
    #                 "else": {"$arrayElemAt": ['$count.total', 0]}
    #             },
    #         },
    #     },
    # }
    ]