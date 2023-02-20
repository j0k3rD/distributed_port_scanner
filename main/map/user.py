from marshmallow import Schema, fields, validate, post_load
from main.models import UserModel


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    mac = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    created_at = fields.DateTime(required=False)

    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)