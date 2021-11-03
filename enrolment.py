from database import db_session
from models import Enrolment, EnrolmentSchema
from utils import admin_only, make_json_response


# GET enrolments
def get_all():
    enrolments = Enrolment.query.order_by(Enrolment.id).all()
    data = EnrolmentSchema(many=True).dump(enrolments)

    return data


# POST enrolments
@admin_only
def create(body, **kwargs):
    user_id = body.get('user_id')
    cohort_id = body.get('cohort_id')
    existing_enrolment = Enrolment.query.filter_by(user_id=user_id)\
        .filter_by(cohort_id=cohort_id).one_or_none()

    if existing_enrolment is None:
        enrolment_schema = EnrolmentSchema()
        enrolment = enrolment_schema.load(body)
        db_session.add(enrolment)
        db_session.commit()
        data = enrolment_schema.dump(enrolment)

        return data, 201
    else:
        title = 'Conflict'
        detail = f'User {user_id} already enrolled to Cohort {cohort_id}'

        return make_json_response(title, 409, detail)


# GET enrolments/<id>
def get_one(id):
    existing_enrolment = Enrolment.query.filter_by(id=id).one_or_none()

    if existing_enrolment is not None:
        data = EnrolmentSchema().dump(existing_enrolment)

        return data
    else:
        title = 'Not Found'
        detail = f'Enrolment {id} not found'

        return make_json_response(title, 404, detail)


# PUT enrolments/<id>
@admin_only
def update(id, body, **kwargs):
    existing_enrolment = Enrolment.query.filter_by(id=id).one_or_none()

    if existing_enrolment is not None:
        enrolment_schema = EnrolmentSchema()
        enrolment = enrolment_schema.load(body)
        enrolment.id = existing_enrolment.id
        db_session.merge(enrolment)
        db_session.commit()
        data = enrolment_schema.dump(existing_enrolment)

        return data
    else:
        title = 'Not Found'
        detail = f'Enrolment {id} not found'

        return make_json_response(title, 404, detail)


# DELETE enrolments/<id>
@admin_only
def delete(id, **kwargs):
    existing_enrolment = Enrolment.query.filter_by(id=id).one_or_none()

    if existing_enrolment is not None:
        db_session.delete(existing_enrolment)
        db_session.commit()
        title = 'OK'
        detail = f'Enrolment {id} deleted'

        return make_json_response(title, 200, detail)
    else:
        title = 'Not Found'
        detail = f'Enrolment {id} not found'

        return make_json_response(title, 404, detail)
