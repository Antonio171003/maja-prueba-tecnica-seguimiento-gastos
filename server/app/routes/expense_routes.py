from flask import Blueprint, request, jsonify
from app.services.expense_service import (
    create_expense, get_expenses,
    get_expense, update_expense, delete_expense, get_summary
)
from app.services.validation_service import validate_expense
from datetime import datetime

expense_bp = Blueprint("expenses", __name__)

@expense_bp.route("", methods=["POST"])
def create():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    missing = [f for f in ["amount", "date", "category_id"] if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    errors = validate_expense(data)
    if errors:
        return jsonify({"errors": errors}), 422

    return jsonify(create_expense(data)), 201

@expense_bp.route("", methods=["GET"])
def list_expenses():
    raw = request.args

    VALID_SORT = {"date_asc", "date_desc", "amount_asc", "amount_desc"}
    sort = raw.get("sort", "date_desc")
    if sort not in VALID_SORT:
        return jsonify({"error": f"Invalid sort value. Options: {', '.join(VALID_SORT)}"}), 400

    filters = {}

    try:
        if "category_id" in raw: filters["category_id"] = int(raw["category_id"])
        if "min_amount"  in raw: filters["min_amount"]  = float(raw["min_amount"])
        if "max_amount"  in raw: filters["max_amount"]  = float(raw["max_amount"])
        if "page"        in raw: filters["page"]        = int(raw["page"])
        if "limit"       in raw: filters["limit"]       = int(raw["limit"])
    except ValueError:
        return jsonify({"error": "category_id, min_amount, max_amount, page and limit must be numeric"}), 400

    try:
        if "start_date" in raw: filters["start_date"] = datetime.strptime(raw["start_date"], "%Y-%m-%d").date()
        if "end_date"   in raw: filters["end_date"]   = datetime.strptime(raw["end_date"],   "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "start_date and end_date must be in YYYY-MM-DD format"}), 400

    filters["sort"] = sort

    return jsonify(get_expenses(filters))

@expense_bp.route("/<int:expense_id>", methods=["GET"])
def get_one(expense_id):
    expense = get_expense(expense_id)
    if expense is None:
        return jsonify({"error": f"Expense {expense_id} not found"}), 404
    return jsonify(expense)

@expense_bp.route("/<int:expense_id>", methods=["PUT"])
def update(expense_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    errors = validate_expense(data)
    if errors:
        return jsonify({"errors": errors}), 422

    expense = update_expense(expense_id, data)
    if expense is None:
        return jsonify({"error": f"Expense {expense_id} not found"}), 404
    return jsonify(expense)

@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
def delete(expense_id):
    if not delete_expense(expense_id):
        return jsonify({"error": f"Expense {expense_id} not found"}), 404
    return "", 204

@expense_bp.route("/summary", methods=["GET"])
def summary():
    raw = request.args
    filters = {}

    try:
        if "category_id" in raw: filters["category_id"] = int(raw["category_id"])
    except ValueError:
        return jsonify({"error": "category_id must be a valid integer"}), 400

    try:
        if "start_date" in raw: filters["start_date"] = datetime.strptime(raw["start_date"], "%Y-%m-%d").date()
        if "end_date"   in raw: filters["end_date"]   = datetime.strptime(raw["end_date"],   "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "start_date and end_date must be in YYYY-MM-DD format"}), 400

    return jsonify(get_summary(filters))
