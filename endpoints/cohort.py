from database import db_session
from models import Cohort
from schemata import CohortSchema
from utils import admin_only


# GET cohorts
def get_all():
    cohorts = Cohort.query.order_by(Cohort.id).all()
    data = CohortSchema(many=True).dump(cohorts)

    return data, 200


# POST cohorts
@admin_only
def create(body, **kwargs):
    cohort_schema = CohortSchema()
    cohort = cohort_schema.load(body)
    db_session.add(cohort)
    db_session.commit()
    data = cohort_schema.dump(cohort)

    return data, 201


# GET cohorts/<id>
def get_one(id):
    existing_cohort = Cohort.query.filter_by(id=id).one_or_none()

    if existing_cohort is not None:
        data = CohortSchema().dump(existing_cohort)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Cohort {id} not found'
        }

        return data, 404


# PUT cohorts/<id>
@admin_only
def update(id, body, **kwargs):
    existing_cohort = Cohort.query.filter_by(id=id).one_or_none()

    if existing_cohort is not None:
        cohort_schema = CohortSchema()
        cohort = cohort_schema.load(body)
        cohort.id = existing_cohort.id
        db_session.merge(cohort)
        db_session.commit()
        data = cohort_schema.dump(existing_cohort)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Cohort {id} not found'
        }

        return data, 404


# DELETE cohorts/<id>
@admin_only
def delete(id, **kwargs):
    cohort = Cohort.query.filter_by(id=id).one_or_none()

    if cohort is not None:
        db_session.delete(cohort)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'Cohort {id} deleted'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Cohort {id} not found'
        }

        return data, 404


# GET cohorts/active
def get_active():
    cohort = Cohort.query.filter_by(is_active=True).one_or_none()

    if cohort is not None:
        data = CohortSchema().dump(cohort)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Active cohort not found'
        }

        return data, 404
