from marshmallow import fields, validates_schema, ValidationError
from marshmallow.validate import Length, Regexp, Range
from app import mm
from app.order_api.models import Order, OrderStatusEnum


class OrderSchema(mm.SQLAlchemyAutoSchema):
    status = fields.Enum(OrderStatusEnum, required=False)
    sender_phone = fields.String(required=True, validate=[Regexp("^((\+?3)?8)?0\d{9}$")])
    receiver_phone = fields.String(required=True, validate=[Regexp("^((\+?3)?8)?0\d{9}$")])
    commodity_name = fields.String(required=True, validate=[Length(max=100)])
    commodity_total_price = fields.Float(required=True, validate=[Range(min=0)])
    sent_date = fields.DateTime(required=False)
    received_date = fields.DateTime(required=False)

    @validates_schema
    def validate_id(self, data, partial, many):
        id = data.get("id")
        if id:
            raise ValidationError("Unknown field.", "id")

    class Meta:
        model = Order
        load_instance = True
