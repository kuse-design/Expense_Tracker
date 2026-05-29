from flask import Flask

from flask_jwt_extended import JWTManager
from app.routes.user_route import user_bp
from app.routes.expense_route import expense_bp
from app.utils.config import Config
from app.Database.database import db

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(expense_bp, url_prefix="/api/expenses")


print(app.url_map)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)