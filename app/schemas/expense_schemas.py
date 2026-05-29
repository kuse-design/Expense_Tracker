from marshmallow import Schema, fields, validate


class ExpenseRequestSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    category = fields.String(required=True, validate=validate.Length(min=1, max=100))


class ExpenseResponseSchema(Schema):
    id = fields.Int()
    amount = fields.Float()
    category = fields.String()
    date = fields.DateTime()
    user_id = fields.Int()