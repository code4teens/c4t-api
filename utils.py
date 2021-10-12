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


def admin_only(f):
    def wrap(**kwargs):
        token_info = kwargs.get('token_info')
        is_admin = token_info.get('is_admin')

        if not is_admin:
            title = 'Forbidden'
            detail = 'Insufficient permission to access resource'

            return make_json_response(title, 403, detail)

        return f(**kwargs)

    return wrap


def admin_or_owner_only(f):
    def wrap(**kwargs):
        id = kwargs.get('id')
        token_info = kwargs.get('token_info')
        sub = token_info.get('sub')
        is_admin = token_info.get('is_admin')

        if not is_admin and sub != id:
            title = 'Forbidden'
            detail = 'Insufficient permission to access resource'

            return make_json_response(title, 403, detail)

        return f(**kwargs)

    return wrap
