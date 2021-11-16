from bson import ObjectId
import re
# câu lệnh query lấy list farm theo ownerId
def searchWeighttype(name):
    return [
        {
        "$match": {
            "name": { "$regex": f'{name}.*' , "$options" :'i' }
        }
    },
    {
        "$project": {
            "id": {
                "$toString": '$_id'
            },
            "_id": 0,
            "name": 1,
            "min": 1,
            "max": 1,
        }
    }
    ]