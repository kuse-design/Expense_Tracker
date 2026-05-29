
from app.Database.database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(75), nullable=False)

    expenses = db.relationship("Expense", backref="user", lazy=True)

