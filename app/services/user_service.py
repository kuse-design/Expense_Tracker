from app import bcrypt
from flask_jwt_extended import create_access_token
from app.Database.database import db
from app.models.user import User
from app.exceptions.bad_request_exception import BadRequestException
from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.conflict_exception import ConflictException
from app.exceptions.Unauthorize_Exception import UnauthorizedException

def hash_password(password: str):
    return bcrypt.generate_password_hash(password).decode("utf-8")

def verify_password(password: str, hashed_password: str):
    return bcrypt.check_password_hash(hashed_password, password)

def register_user(request):
    email = request["email"]
    password = request["password"]

    if not email or not password:
        raise BadRequestException("Email or password is required")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise ConflictException("User already exists")

    hashed_password = hash_password(password)

    user = User(email=email, password=hashed_password)

    db.session.add(user)
    db.session.commit()

    return user

def login_user(data):
    email = data["email"]
    password = data["password"]

    if not email or not password:
        raise BadRequestException("Email and password are required")

    user = User.query.filter_by(email=email).first()

    if not user or not verify_password(password, user.password):
        raise UnauthorizedException("Invalid credentials")

    access_token = create_access_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "user": user
    }

def get_user_by_id(user_id):
    user = User.query.get(int(user_id))
    if not user:
        raise NotFoundException("User not found")
    return user