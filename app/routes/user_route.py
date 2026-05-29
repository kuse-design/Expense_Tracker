from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import register_user, login_user
from app.schemas.user_schemas import UserRequestSchema, UserResponseSchema
from app.services.user_service import get_user_by_id

user_bp = Blueprint("users", __name__)
user_request_schema = UserRequestSchema()
user_response_schema = UserResponseSchema()


@user_bp.route("/register", methods=["POST"])
def register():
    data = user_request_schema.load(request.get_json())
    user = register_user(data)

    return {
        "user": user_response_schema.dump(user)
    }, 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    result = login_user(data)

    return {
        "access_token": result["access_token"],
        "user": user_response_schema.dump(result["user"])
    }, 200


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = get_user_by_id(user_id)

    return user_response_schema.dump(user), 200