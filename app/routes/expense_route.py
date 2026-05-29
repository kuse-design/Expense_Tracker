from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.expense_schemas import ExpenseRequestSchema, ExpenseResponseSchema
from app.services.expense_service import (
    create_expense,
    get_expenses,
    update_expense,
    delete_expense,
    get_monthly_expenses,
    filter_expense as filter_expense_service
)

expense_bp = Blueprint("expense", __name__)

expense_request_schema = ExpenseRequestSchema()
expense_response_schema = ExpenseResponseSchema()
expense_response_schemas = ExpenseResponseSchema(many=True)


@expense_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    user_id = int(get_jwt_identity())
    data = expense_request_schema.load(request.get_json())

    expense = create_expense(data, user_id)

    return expense_response_schema.dump(expense), 201


@expense_bp.route("/view-all", methods=["GET"])
@jwt_required()
def get_all():
    user_id = int(get_jwt_identity())

    expenses = get_expenses(user_id)

    return expense_response_schemas.dump(expenses), 200


@expense_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update(expense_id):
    user_id = int(get_jwt_identity())
    data = expense_request_schema.load(request.get_json(), partial=True)

    expense = update_expense(expense_id, data, user_id)

    return expense_response_schema.dump(expense), 200


@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete(expense_id):
    user_id = int(get_jwt_identity())

    delete_expense(expense_id, user_id)

    return {"message": "Deleted"}, 200


@expense_bp.route("/filter", methods=["GET"])
@jwt_required()
def filter_expense():
    user_id = int(get_jwt_identity())

    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    expenses = filter_expense_service(user_id, category, start_date, end_date)

    return expense_response_schemas.dump(expenses), 200


@expense_bp.route("/monthly", methods=["GET"])
@jwt_required()
def monthly_summary():
    user_id = int(get_jwt_identity())

    summary = get_monthly_expenses(user_id)

    return {
        "month": summary["month"],
        "total": summary["total"],
        "count": summary["count"],
        "expenses": expense_response_schemas.dump(summary["expenses"])
    }, 200