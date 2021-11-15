from flask import jsonify

def successResponse(dataZip):
    return jsonify(data=dataZip, statusCode='OK')

def failedResponse(message: str, statusCode: str):
    return jsonify(message=message, statusCode=statusCode)