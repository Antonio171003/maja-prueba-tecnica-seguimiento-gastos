from app.extensions import db
from app.models.expense import Expense
from app.models.category import Category 
from sqlalchemy import func
from datetime import datetime

def create_expense(data):
    expense = Expense(
        amount=data["amount"],
        description=data.get("description"),
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        category_id=data["category_id"]
    )

    db.session.add(expense)
    db.session.commit()

    return _serialize(expense)

def get_expenses(filters):
    query = Expense.query

    if "category_id" in filters:
        query = query.filter_by(category_id=filters["category_id"])

    if "start_date" in filters:
        query = query.filter(Expense.date >= filters["start_date"])
    if "end_date" in filters:
        query = query.filter(Expense.date <= filters["end_date"])

    if "min_amount" in filters:
        query = query.filter(Expense.amount >= filters["min_amount"])
    if "max_amount" in filters:
        query = query.filter(Expense.amount <= filters["max_amount"])

    sort = filters.get("sort", "date_desc")
    sort_options = {
        "date_asc":    Expense.date.asc(),
        "date_desc":   Expense.date.desc(),
        "amount_asc":  Expense.amount.asc(),
        "amount_desc": Expense.amount.desc(),
    }
    query = query.order_by(sort_options.get(sort, Expense.date.desc()))

    page  = int(filters.get("page",  1))
    limit = int(filters.get("limit", 20))
    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return {
        "data":  [_serialize(e) for e in pagination.items],
        "total": pagination.total,
        "page":  pagination.page,
        "pages": pagination.pages,
        "limit": limit,
    }

def get_expense(expense_id):
    expense = db.session.get(Expense, expense_id)
    return _serialize(expense) if expense else None

def update_expense(expense_id, data):
    expense = db.session.get(Expense, expense_id)
    if expense is None:
        return None

    if "amount"      in data: expense.amount      = data["amount"]
    if "description" in data: expense.description = data["description"]
    if "date"        in data: expense.date        = datetime.strptime(data["date"], "%Y-%m-%d")
    if "category_id" in data: expense.category_id = data["category_id"]

    db.session.commit()
    return _serialize(expense)

def delete_expense(expense_id):
    expense = db.session.get(Expense, expense_id)
    if expense is None:
        return False
    db.session.delete(expense)
    db.session.commit()
    return True

def get_summary(filters):
    query = db.session.query(
        Category.id,
        Category.name,
        func.count(Expense.id).label("count"),
        func.sum(Expense.amount).label("total"),
    ).join(Expense, Expense.category_id == Category.id)

    if "category_id" in filters:
        query = query.filter(Expense.category_id == filters["category_id"])
    if "start_date" in filters:
        query = query.filter(Expense.date >= filters["start_date"])
    if "end_date" in filters:
        query = query.filter(Expense.date <= filters["end_date"])

    rows = query.group_by(Category.id, Category.name).all()

    by_category = [
        {
            "category_id":   row.id,
            "category_name": row.name,
            "count":         row.count,
            "total":         float(row.total),
        }
        for row in rows
    ]

    grand_total = sum(r["total"] for r in by_category)
    grand_count = sum(r["count"] for r in by_category)

    return {
        "total":       grand_total,
        "count":       grand_count,
        "by_category": by_category,
    }

def _serialize(expense):
    return {
        "id":          expense.id,
        "amount":      float(expense.amount),
        "description": expense.description,
        "date":        expense.date.isoformat() if expense.date else None,
        "category_id": expense.category_id,
        "created_at":  expense.created_at.isoformat() if expense.created_at else None,
    }

