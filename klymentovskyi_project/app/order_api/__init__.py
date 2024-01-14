from flask import Blueprint
from flask_restful import Api
from .views import OrdersApi, OrderApi

order_api_blueprint = Blueprint("order", __name__, url_prefix="/order")
api = Api(order_api_blueprint)

api.add_resource(OrdersApi, "/")
api.add_resource(OrderApi, "/<int:id>")
