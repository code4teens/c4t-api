from database import db_session
from models import Enrolment
from schemata import EnrolmentSchema
from utils import admin_only


# GET enrolments
def get_all():
    enrolments = Enrolment.query.order_by(Enrolment.id).all()
    data = EnrolmentSchema(many=True).dump(enrolments)

    return data, 200


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
        data = {
            'title': 'Conflict',
            'status': 409,
            'detail': 'Enrolment with posted details already exists'
        }

        return data, 409


# GET enrolments/<id>
def get_one(id):
    enrolment = Enrolment.query.filter_by(id=id).one_or_none()

    if enrolment is not None:
        data = EnrolmentSchema().dump(enrolment)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Enrolment {id} not found'
        }

        return data, 404


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

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Enrolment {id} not found'
        }

        return data, 404


# DELETE enrolments/<id>
@admin_only
def delete(id, **kwargs):
    enrolment = Enrolment.query.filter_by(id=id).one_or_none()

    if enrolment is not None:
        db_session.delete(enrolment)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'Enrolment {id} deleted'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Enrolment {id} not found'
        }

        return data, 404
