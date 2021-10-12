from flask import jsonify, make_response
import pytz

tz = pytz.timezone('Asia/Kuala_Lumpur')


def make_json_response(title, status, detail):
    response_object = {
        'title': title,
        'status': status,
        'detail': detail
    }

    return make_response(jsonify(response_object)), status
