
from app.Database.database import db
from app.models.expense import Expense
from app.exceptions.bad_request_exception import BadRequestException
from app.exceptions.not_found_exception import NotFoundException
from datetime import datetime

def create_expense(request, user_id):
    amount = request["amount"]
    category = request["category"]

    if not amount or amount <= 0:
        raise BadRequestException("Invalid amount")

    if not category:
        raise BadRequestException("Invalid category")

    expense = Expense(amount=amount, category=category, user_id=user_id)

    db.session.add(expense)
    db.session.commit()

    return expense

def get_expenses(user_id):
    return Expense.query.filter_by(user_id=user_id).all()

def update_expense(expense_id, request, user_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

    if not expense:
        raise NotFoundException("Expense not found")

    if "amount" in request:
        if request["amount"] <= 0:
            raise BadRequestException("Invalid amount")
        expense.amount = request["amount"]

    if "category" in request:
        expense.category = request["category"]

    db.session.commit()

    return expense


def delete_expense(expense_id, user_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

    if not expense:
        raise NotFoundException("Expense not found")

    db.session.delete(expense)
    db.session.commit()


def filter_expense(user_id, category = None):
    query = Expense.query.filter_by(user_id = user_id).all()

    if category:
        query = query.filter_by(category = category)
    expense = query.all()

    return [expense.to_dict() for expense in expense]

def get_monthly_expenses(user_id):
    now = datetime.utcnow()
    expenses = Expense.query.filter_by(user_id = user_id).all()

    total = 0
    for Exp in expenses:
        if Exp.date.month == now.month and Exp.date.year == now.year:
            total += Exp.amount

    return {"month": now.month, "total": total}

