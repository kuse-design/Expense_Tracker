import bcrypt
from app.models.user import db, User

def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def register_user(request):
    email = request.get("email")
    password = request.get("password")

    if not email or not password:
        return {"error": "user already exists"}

    hashed_password = hash_password(password)

    user = User(email = email, password = hashed_password)
    db.session.add(user)
    db.session.commit()

    return {"message": "user created", "user": user.to_dict()}

def login_user(request):
    email = request.get("email")
    password = request.get("password")

    user = User.query.filter_by(email = email).first()

    if not user or not verify_password(password, user.password):
        return {"error": "Invalid credentials"}

    return  {"message": "Login successful", "user": user.to_dict()}
