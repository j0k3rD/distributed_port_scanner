from marshmallow import Schema, fields, validate, post_load, post_dump
from main.models import User


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    mac = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)