from marshmallow import fields, post_load, Schema

from models import Bot, Channel, Cohort, Enrolment, Eval, User


class UserSchema(Schema):
    id = fields.Integer()
    password = fields.String(load_only=True)
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    xp = fields.Integer()
    is_admin = fields.Boolean()
    api_key = fields.String()
    created_at = fields.DateTime(dump_only=True)
    last_updated = fields.DateTime(dump_only=True)

    bots = fields.Nested(
        'NestedUserBotSchema', default=[], many=True, dump_only=True
    )
    channels = fields.Nested(
        'NestedUserChannelSchema', default=[], many=True, dump_only=True
    )
    enrolments = fields.Nested(
        'NestedUserEnrolmentSchema', default=[], many=True, dump_only=True
    )
    evals_as_evaluator = fields.Nested(
        'NestedEvaluatorEvalSchema', default=[], many=True, dump_only=True
    )
    evals_as_evaluatee = fields.Nested(
        'NestedEvaluateeEvalSchema', default=[], many=True, dump_only=True
    )

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class NestedUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    discriminator = fields.String(dump_only=True)
    display_name = fields.String(dump_only=True)


class BotSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    user_id = fields.Integer(load_only=True)
    cohort_id = fields.Integer(load_only=True)
    msg_id = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    last_updated = fields.DateTime(dump_only=True)

    user = fields.Nested('NestedUserSchema', dump_only=True)
    cohort = fields.Nested('NestedCohortSchema', dump_only=True)

    @post_load
    def make_bot(self, data, **kwargs):
        return Bot(**data)


class NestedUserBotSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    discriminator = fields.String(dump_only=True)
    display_name = fields.String(dump_only=True)

    cohort = fields.Nested('NestedCohortSchema', dump_only=True)


class NestedCohortBotSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    discriminator = fields.String(dump_only=True)
    display_name = fields.String(dump_only=True)

    user = fields.Nested('NestedUserSchema', dump_only=True)


class ChannelSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    user_id = fields.Integer(load_only=True)
    cohort_id = fields.Integer(load_only=True)
    created_at = fields.DateTime(dump_only=True)
    last_updated = fields.DateTime(dump_only=True)

    user = fields.Nested('NestedUserSchema', dump_only=True)
    cohort = fields.Nested('NestedCohortSchema', dump_only=True)

    @post_load
    def make_channel(self, data, **kwargs):
        return Channel(**data)


class NestedUserChannelSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)

    cohort = fields.Nested('NestedCohortSchema', dump_only=True)


class NestedCohortChannelSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)

    user = fields.Nested('NestedUserSchema', dump_only=True)


class CohortSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    nickname = fields.String()
    duration = fields.Integer()
    start_date = fields.Date()
    is_active = fields.Boolean(allow_none=True)
    review_schema = fields.Dict(allow_none=True)
    feedback_schema = fields.Dict(allow_none=True)

    bots = fields.Nested(
        'NestedCohortBotSchema', default=[], many=True, dump_only=True
    )
    channels = fields.Nested(
        'NestedCohortChannelSchema', default=[], many=True, dump_only=True
    )
    enrolments = fields.Nested(
        'NestedCohortEnrolmentSchema', default=[], many=True, dump_only=True
    )
    evals = fields.Nested(
        'NestedCohortEvalSchema', default=[], many=True, dump_only=True
    )

    @post_load
    def make_cohort(self, data, **kwargs):
        return Cohort(**data)


class NestedCohortSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    nickname = fields.String(dump_only=True)


class EnrolmentSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(load_only=True)
    cohort_id = fields.Integer(load_only=True)

    user = fields.Nested('NestedUserSchema', dump_only=True)
    cohort = fields.Nested('NestedCohortSchema', dump_only=True)

    @post_load
    def make_enrolment(self, data, **kwargs):
        return Enrolment(**data)


class NestedUserEnrolmentSchema(Schema):
    id = fields.Integer(dump_only=True)

    cohort = fields.Nested('NestedCohortSchema', dump_only=True)


class NestedCohortEnrolmentSchema(Schema):
    id = fields.Integer(dump_only=True)

    user = fields.Nested('NestedUserSchema', dump_only=True)


class EvalSchema(Schema):
    id = fields.Integer(dump_only=True)
    evaluator_id = fields.Integer(load_only=True)
    evaluatee_id = fields.Integer(load_only=True)
    cohort_id = fields.Integer(load_only=True)
    date = fields.Date()
    review = fields.Dict(allow_none=True)
    feedback = fields.Dict(allow_none=True)

    evaluator = fields.Nested('NestedUserSchema', dump_only=True)
    evaluatee = fields.Nested('NestedUserSchema', dump_only=True)
    cohort = fields.Nested('NestedCohortSchema', dump_only=True)

    @post_load
    def make_eval(self, data, **kwargs):
        return Eval(**data)


class NestedEvaluatorEvalSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(dump_only=True)

    evaluatee = fields.Nested('NestedUserSchema', dump_only=True)
    cohort = fields.Nested('NestedCohortSchema', dump_only=True)


class NestedEvaluateeEvalSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(dump_only=True)

    evaluator = fields.Nested('NestedUserSchema', dump_only=True)
    cohort = fields.Nested('NestedCohortSchema', dump_only=True)


class NestedCohortEvalSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(dump_only=True)

    evaluator = fields.Nested('NestedUserSchema', dump_only=True)
    evaluatee = fields.Nested('NestedUserSchema', dump_only=True)
