from flask import jsonify, make_response


def make_json_response(status, code, message):
    response_object = {
        'status': status,
        'code': code,
        'message': message
    }

    return make_response(jsonify(response_object)), code
