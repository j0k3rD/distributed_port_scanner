from marshmallow import Schema, fields, validate, post_load, post_dump
from main.models.scanner import Scanner


class ScannerSchema(Schema):
    id = fields.Int(dump_only=True)
    scanner_type = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    ip = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    port = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    created_at = fields.DateTime(dump_only=True)
    result = fields.Str(dump_only=True)
    user_id = fields.Int(required=True)
    user = fields.Nested('UserSchema')

    @post_load
    def make_scanner(self, data, **kwargs):
        return Scanner(**data)

    SKIP_VALUES = ['user_id']
    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {key: value for key, value in data.items() if key not in self.SKIP_VALUES}