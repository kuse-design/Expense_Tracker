from app.models.expense import db, Expense
from datetime import datetime

def create_expense(request, user_id):
    amount = request.get("amount")
    category = request.get("category")

    if not amount or amount <= 0:
        return {"error": "Invalid amount"}

    if not category:
        return {"error": "Invalid category"}

    return  Expense(amount = amount, category = category, user_id = user_id)

def get_expenses(user_id):
    expenses = Expense.query.filter_by(user_id = user_id).all()
    return [expense.to_dict() for expense in expenses]

def update_expense(expense_id, request, user_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

    if not expense:
        return {"error": "Expense not found"}

    if "amount" in request:
        if request["amount"] <= 0:
            return {"error": "Invalid amount"}
        expense.amount = request["amount"]

    if "category" in request:
        expense.category = request["category"]

    db.session.commit()

    return {
        "message": "updated",
        "expense": expense.to_dict()
    }

def delete_expense(expense_id, user_id):
        expense = Expense.query.filter_by(id = expense_id, user_id = user_id).first()

        if not expense:
            return {"error": "Invalid expense not found"}

        db.session.delete(expense)
        db.session.commit()

        return {"message": "Delete successfully"}

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

