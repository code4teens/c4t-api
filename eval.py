from database import db_session
from models import Eval, EvalSchema
from utils import admin_only, make_json_response


# GET evals
def get_all():
    evals = Eval.query.order_by(Eval.id).all()
    data = EvalSchema(many=True).dump(evals)

    return data


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
        title = 'Conflict'
        detail = f'Eval with abovementioned details already exists'

        return make_json_response(title, 409, detail)


# GET evals/<id>
def get_one(id):
    existing_eval = Eval.query.filter_by(id=id).one_or_none()

    if existing_eval is not None:
        data = EvalSchema().dump(existing_eval)

        return data
    else:
        title = 'Not Found'
        detail = f'Eval {id} not found'

        return make_json_response(title, 404, detail)


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

        return data
    else:
        title = 'Not Found'
        detail = f'Eval {id} not found'

        return make_json_response(title, 404, detail)


# DELETE evals/<id>
@admin_only
def delete(id, **kwargs):
    existing_eval = Eval.query.filter_by(id=id).one_or_none()

    if existing_eval is not None:
        db_session.delete(existing_eval)
        db_session.commit()
        title = 'OK'
        detail = f'Eval {id} deleted'

        return make_json_response(title, 200, detail)
    else:
        title = 'Not Found'
        detail = f'Eval {id} not found'

        return make_json_response(title, 404, detail)
