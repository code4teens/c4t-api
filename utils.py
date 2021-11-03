from functools import wraps

import pytz

tz = pytz.timezone('Asia/Kuala_Lumpur')


def admin_only(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        token_info = kwargs.get('token_info')
        is_admin = token_info.get('is_admin')

        if not is_admin:
            data = {
                'title': 'Forbidden',
                'status': 403,
                'detail': 'Insufficient permission to access resource'
            }

            return data, 403

        return func(*args, **kwargs)

    return decorated_view


def admin_or_owner_only(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        id = kwargs.get('id')
        token_info = kwargs.get('token_info')
        sub = token_info.get('sub')
        is_admin = token_info.get('is_admin')

        if not is_admin and sub != id:
            data = {
                'title': 'Forbidden',
                'status': 403,
                'detail': 'Insufficient permission to access resource'
            }

            return data, 403

        return func(**kwargs)

    return decorated_view
