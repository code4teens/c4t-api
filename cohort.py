from database import db_session
from models import Cohort, CohortSchema
from utils import admin_only, make_json_response


# GET cohorts
def get_all():
    cohorts = Cohort.query.order_by(Cohort.id).all()
    data = CohortSchema(many=True).dump(cohorts)

    return data


# POST cohorts
@admin_only
def create(body, **kwargs):
    id = body.get('id')
    existing_cohort = Cohort.query.filter_by(id=id).one_or_none()

    if existing_cohort is None:
        cohort_schema = CohortSchema()
        cohort = cohort_schema.load(body)
        db_session.add(cohort)
        db_session.commit()
        data = cohort_schema.dump(cohort)

        return data, 201
    else:
        title = 'Conflict'
        detail = f'Cohort {id} already exists'

        return make_json_response(title, 409, detail)


# GET cohorts/<id>
def get_one(id):
    existing_cohort = Cohort.query.filter_by(id=id).one_or_none()

    if existing_cohort is not None:
        data = CohortSchema().dump(existing_cohort)

        return data
    else:
        title = 'Not Found'
        detail = f'Cohort {id} not found'

        return make_json_response(title, 404, detail)


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

        return data
    else:
        title = 'Not Found'
        detail = f'Cohort {id} not found'

        return make_json_response(title, 404, detail)


# DELETE cohorts/<id>
@admin_only
def delete(id, **kwargs):
    existing_cohort = Cohort.query.filter_by(id=id).one_or_none()

    if existing_cohort is not None:
        db_session.delete(existing_cohort)
        db_session.commit()
        title = 'OK'
        detail = f'Cohort {id} deleted'

        return make_json_response(title, 200, detail)
    else:
        title = 'Not Found'
        detail = f'Cohort {id} not found'

        return make_json_response(title, 404, detail)


# PUT cohorts/<id>/review_schema
@admin_only
def update_review_schema(**kwargs):
    update(**kwargs)


# PUT cohorts/<id>/feedback_schema
@admin_only
def update_feedback_schema(**kwargs):
    update(**kwargs)
