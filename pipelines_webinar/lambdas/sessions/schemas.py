from lambdas.sessions.deps.marshmallow import Schema, fields, post_load
from sessions.models import Session


class SessionSchema(Schema):
    uid = fields.Str()
    username = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    expires_at = fields.DateTime(dump_only=True)
    ttl = fields.Integer(dump_only=True)

    @post_load
    def make_session(self, data, **kwargs):
        return Session(**data)
