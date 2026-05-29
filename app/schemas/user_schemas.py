from marshmallow import Schema, fields, validate




class UserRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))


class UserResponseSchema(Schema):
    id = fields.Int()
    email = fields.Email()

