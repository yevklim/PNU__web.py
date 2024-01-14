from app import db
from flask import request
from flask_restful import Resource
from app.order_api.models import Order
from .schemas.order import OrderSchema


class OrdersApi(Resource):
    def get(self):
        schema = OrderSchema(many=True)
        orders = Order.query.all()
        return schema.dump(orders)

    def post(self):
        schema = OrderSchema()
        order = schema.load(request.json)
        db.session.add(order)
        db.session.commit()
        return schema.dump(order)


class OrderApi(Resource):
    def get(self, id):
        schema = OrderSchema(partial=True)
        order = Order.query.filter_by(id=id).first_or_404(description='Order not found.')
        return schema.dump(order)

    def put(self, id):
        schema = OrderSchema(partial=True)
        order = Order.query.filter_by(id=id).first_or_404(description='Order not found.')
        order = schema.load(request.json, instance=order)
        db.session.add(order)
        db.session.commit()
        return schema.dump(order)

    def delete(self, id):
        schema = OrderSchema()
        order = Order.query.filter_by(id=id).first_or_404(description='Order not found.')
        db.session.delete(order)
        db.session.commit()
        return schema.dump(order)
