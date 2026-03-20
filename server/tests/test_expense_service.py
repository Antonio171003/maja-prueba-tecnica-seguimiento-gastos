from app.extensions import db


def _create_category(app, name="Food"):
    from app.models import Category
    with app.app_context():
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category.id


# CREATE

def test_create_expense_service(app):
    from app.models import Expense
    from app.services.expense_service import create_expense

    category_id = _create_category(app)

    with app.app_context():
        result = create_expense({
            "amount": 150.50, "description": "Groceries",
            "date": "2026-03-18", "category_id": category_id,
        })

        assert result["id"] is not None
        assert result["amount"] == 150.5
        assert result["description"] == "Groceries"
        assert result["date"] == "2026-03-18"

        saved = db.session.get(Expense, result["id"])
        assert float(saved.amount) == 150.5
        assert saved.category_id == category_id


# GET ALL

def test_get_expenses_returns_all(app):
    from app.models import Category, Expense
    from app.services.expense_service import get_expenses

    with app.app_context():
        food = Category(name="Food")
        transport = Category(name="Transport")
        db.session.add_all([food, transport])
        db.session.commit()

        db.session.add_all([
            Expense(amount=100.00, description="Lunch", date="2026-03-18", category_id=food.id),
            Expense(amount=60.00,  description="Bus",   date="2026-03-18", category_id=transport.id),
        ])
        db.session.commit()

        result = get_expenses({})

        assert result["total"] == 2
        descriptions = {e["description"] for e in result["data"]}
        assert descriptions == {"Lunch", "Bus"}


def test_get_expenses_filters_by_category_id(app):
    from app.models import Category, Expense
    from app.services.expense_service import get_expenses

    with app.app_context():
        food = Category(name="Food")
        transport = Category(name="Transport")
        db.session.add_all([food, transport])
        db.session.commit()

        db.session.add_all([
            Expense(amount=100.00, description="Lunch", date="2026-03-18", category_id=food.id),
            Expense(amount=60.00,  description="Bus",   date="2026-03-18", category_id=transport.id),
        ])
        db.session.commit()

        result = get_expenses({"category_id": food.id})

        assert result["total"] == 1
        assert result["data"][0]["description"] == "Lunch"


def test_get_expenses_returns_empty_list_when_no_rows(app):
    from app.services.expense_service import get_expenses

    with app.app_context():
        result = get_expenses({})

        assert result["data"] == []
        assert result["total"] == 0

# GET BY ID

def test_get_expense_returns_expense(app):
    from app.services.expense_service import create_expense, get_expense

    category_id = _create_category(app)

    with app.app_context():
        created = create_expense({
            "amount": 50.00, "description": "Coffee",
            "date": "2026-03-18", "category_id": category_id,
        })
        result = get_expense(created["id"])

        assert result is not None
        assert result["description"] == "Coffee"


def test_get_expense_returns_none_when_not_found(app):
    from app.services.expense_service import get_expense

    with app.app_context():
        assert get_expense(9999) is None


# UPDATE

def test_update_expense_changes_fields(app):
    from app.services.expense_service import create_expense, update_expense

    category_id = _create_category(app)

    with app.app_context():
        created = create_expense({
            "amount": 50.00, "description": "Coffee",
            "date": "2026-03-18", "category_id": category_id,
        })
        result = update_expense(created["id"], {"amount": 99.00, "description": "Fancy Coffee"})

        assert result["amount"] == 99.00
        assert result["description"] == "Fancy Coffee"


def test_update_expense_returns_none_when_not_found(app):
    from app.services.expense_service import update_expense

    with app.app_context():
        assert update_expense(9999, {"amount": 10}) is None


# DELETE

def test_delete_expense_removes_record(app):
    from app.services.expense_service import create_expense, delete_expense, get_expense

    category_id = _create_category(app)

    with app.app_context():
        created = create_expense({
            "amount": 50.00, "description": "Coffee",
            "date": "2026-03-18", "category_id": category_id,
        })
        assert delete_expense(created["id"]) is True
        assert get_expense(created["id"]) is None


def test_delete_expense_returns_false_when_not_found(app):
    from app.services.expense_service import delete_expense

    with app.app_context():
        assert delete_expense(9999) is False