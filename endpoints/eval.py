from database import db_session
from models import Eval
from schemata import EvalSchema
from utils import admin_only


# GET evals
def get_all():
    evals = Eval.query.order_by(Eval.id).all()
    data = EvalSchema(many=True).dump(evals)

    return data, 200


# POST evals
@admin_only
def create(body, **kwargs):
    evaluator_id = body.get('evaluator_id')
    evaluatee_id = body.get('evaluatee_id')
    cohort_id = body.get('cohort_id')
    date = body.get('date')
    existing_eval = Eval.query.filter_by(evaluator_id=evaluator_id)\
        .filter_by(evaluatee_id=evaluatee_id)\
        .filter_by(cohort_id=cohort_id)\
        .filter_by(date=date)\
        .one_or_none()

    if existing_eval is None:
        eval_schema = EvalSchema()
        eval = eval_schema.load(body)
        db_session.add(eval)
        db_session.commit()
        data = eval_schema.dump(eval)

        return data, 201
    else:
        data = {
            'title': 'Conflict',
            'status': 409,
            'detail': 'Eval with posted details already exists'
        }

        return data, 409


# GET evals/<id>
def get_one(id):
    eval = Eval.query.filter_by(id=id).one_or_none()

    if eval is not None:
        data = EvalSchema().dump(eval)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Eval {id} not found'
        }

        return data, 404


# PUT evals/<id>
@admin_only
def update(id, body, **kwargs):
    existing_eval = Eval.query.filter_by(id=id).one_or_none()

    if existing_eval is not None:
        eval_schema = EvalSchema()
        eval = eval_schema.load(body)
        eval.id = existing_eval.id
        db_session.merge(eval)
        db_session.commit()
        data = eval_schema.dump(existing_eval)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Eval {id} not found'
        }

        return data, 404


# DELETE evals/<id>
@admin_only
def delete(id, **kwargs):
    eval = Eval.query.filter_by(id=id).one_or_none()

    if eval is not None:
        db_session.delete(eval)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'Eval {id} deleted'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Eval {id} not found'
        }

        return data, 404
