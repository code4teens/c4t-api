from flask import jsonify, make_response
import pytz

tz = pytz.timezone('Asia/Kuala_Lumpur')


def make_json_response(status, code, message):
    response_object = {
        'status': status,
        'code': code,
        'message': message
    }

    return make_response(jsonify(response_object)), code
