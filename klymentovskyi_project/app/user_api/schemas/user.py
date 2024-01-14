from marshmallow import fields, validates_schema, ValidationError
from marshmallow.validate import Email, Length
from app import mm
from app.user.models import User


class UserSchema(mm.SQLAlchemyAutoSchema):
    email = fields.String(required=True, validate=[Email(), Length(max=120)])
    username = fields.String(required=True, validate=[Length(min=4, max=20)])
    password = fields.String(required=True, validate=[Length(min=6, max=60)])

    @validates_schema
    def validate_id(self, data, partial, many):
        id = data.get("id")
        if id:
            raise ValidationError("ID mustn't be set directly.", "id")

    @validates_schema
    def validate_email(self, data, partial, many):
        email = data.get("email")
        if self.instance and self.instance.email == email:
            return
        if User.query.filter_by(email=email).first():
            raise ValidationError("E-mail already registered.", "email")

    @validates_schema
    def validate_username(self, data, partial, many):
        username = data.get("username")
        if self.instance and self.instance.username == username:
            return
        if User.query.filter_by(username=username).first():
            raise ValidationError("Username already in use.", "username")

    @validates_schema
    def validate_passhash(self, data, partial, many):
        password_hash = data.get("password_hash")
        if password_hash:
            raise ValidationError("Password hash mustn't be set directly.", "password_hash")

    @validates_schema
    def validate_lastseen(self, data, partial, many):
        last_seen = data.get("last_seen")
        if last_seen:
            raise ValidationError("Last seen date mustn't be set directly.", "last_seen")

    @validates_schema
    def validate_image_file(self, data, partial, many):
        image_file = data.get("image_file")
        if image_file:
            raise ValidationError("Image file mustn't be set directly.", "image_file")

    class Meta:
        model = User
        load_instance = True
