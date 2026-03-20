from datetime import datetime
from app.models.category import Category
from app.extensions import db

def validate_expense(data):

    errors = []

    if "amount" in data:
        try:
            amount = float(data["amount"])
            if amount <= 0:
                errors.append("amount must be greater than 0")
        except (TypeError, ValueError):
            errors.append("amount must be a valid number")

    if "date" in data:
        try:
            datetime.strptime(data["date"], "%Y-%m-%d")
        except (TypeError, ValueError):
            errors.append("date must be in YYYY-MM-DD format")

    if "category_id" in data:
        try:
            cat_id = int(data["category_id"])
            if not db.session.get(Category, cat_id):
                errors.append(f"category_id {cat_id} does not exist")
        except (TypeError, ValueError):
            errors.append("category_id must be a valid integer")

    return errors
