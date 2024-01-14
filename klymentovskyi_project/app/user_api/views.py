from app import db
from flask import request
from flask_restful import Resource
from app.user.models import User
from .schemas.user import UserSchema


class RegisterUserApi(Resource):
    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return schema.dump(user)


class UserApi(Resource):
    def get(self, id):
        schema = UserSchema(partial=True)
        user = User.query.filter_by(id=id).first_or_404(description='User not found.')

        return schema.dump(user)

    def put(self, id):
        schema = UserSchema(partial=True)
        user = User.query.filter_by(id=id).first_or_404(description='User not found.')

        user = schema.load(request.json, instance=user)
        db.session.add(user)
        db.session.commit()

        return schema.dump(user)

    def delete(self, id):
        schema = UserSchema()
        user = User.query.filter_by(id=id).first_or_404(description='User not found.')

        db.session.delete(user)
        db.session.commit()

        return schema.dump(user)
