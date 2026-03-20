def create_category(client, name):
    r = client.post("/categories", json={"name": name})
    assert r.status_code == 201
    return r.get_json()


def create_expense(client, amount, description, date, category_id):
    r = client.post("/expenses", json={
        "amount": amount, "description": description,
        "date": date, "category_id": category_id
    })
    assert r.status_code == 201
    return r.get_json()


def _seed(client):
    food      = create_category(client, "Food")
    transport = create_category(client, "Transport")

    create_expense(client, 100.00, "Lunch",  "2026-03-01", food["id"])
    create_expense(client, 200.00, "Dinner", "2026-03-15", food["id"])
    create_expense(client,  60.00, "Bus",    "2026-03-10", transport["id"])

    return food, transport


# SUMMARY GENERAL

def test_summary_totals(client):
    _seed(client)
    body = client.get("/expenses/summary").get_json()

    assert body["total"] == 360.00
    assert body["count"] == 3
    assert len(body["by_category"]) == 2


def test_summary_by_category_values(client):
    _seed(client)
    body = client.get("/expenses/summary").get_json()

    food_row = next(r for r in body["by_category"] if r["category_name"] == "Food")
    assert food_row["total"] == 300.00
    assert food_row["count"] == 2

    transport_row = next(r for r in body["by_category"] if r["category_name"] == "Transport")
    assert transport_row["total"] == 60.00
    assert transport_row["count"] == 1


def test_summary_empty(client):
    body = client.get("/expenses/summary").get_json()

    assert body["total"] == 0
    assert body["count"] == 0
    assert body["by_category"] == []


# SUMMARY CON FILTROS

def test_summary_filter_by_category(client):
    food, _ = _seed(client)
    body = client.get(f"/expenses/summary?category_id={food['id']}").get_json()

    assert body["total"] == 300.00
    assert body["count"] == 2
    assert len(body["by_category"]) == 1


def test_summary_filter_by_date_range(client):
    _seed(client)
    body = client.get("/expenses/summary?start_date=2026-03-05&end_date=2026-03-12").get_json()

    assert body["total"] == 60.00
    assert body["count"] == 1


def test_summary_invalid_date(client):
    response = client.get("/expenses/summary?start_date=01-03-2026")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_summary_invalid_category_id(client):
    response = client.get("/expenses/summary?category_id=abc")
    assert response.status_code == 400


# VALIDACIONES AL CREAR

def test_create_expense_amount_zero(client):
    food = create_category(client, "Food")
    response = client.post("/expenses", json={
        "amount": 0, "date": "2026-03-18", "category_id": food["id"]
    })
    assert response.status_code == 422
    assert "errors" in response.get_json()


def test_create_expense_negative_amount(client):
    food = create_category(client, "Food")
    response = client.post("/expenses", json={
        "amount": -50, "date": "2026-03-18", "category_id": food["id"]
    })
    assert response.status_code == 422


def test_create_expense_invalid_amount_type(client):
    food = create_category(client, "Food")
    response = client.post("/expenses", json={
        "amount": "mucho", "date": "2026-03-18", "category_id": food["id"]
    })
    assert response.status_code == 422


def test_create_expense_invalid_date_format(client):
    food = create_category(client, "Food")
    response = client.post("/expenses", json={
        "amount": 100, "date": "18/03/2026", "category_id": food["id"]
    })
    assert response.status_code == 422


def test_create_expense_nonexistent_category(client):
    response = client.post("/expenses", json={
        "amount": 100, "date": "2026-03-18", "category_id": 9999
    })
    assert response.status_code == 422
    errors = response.get_json()["errors"]
    assert any("category_id" in e for e in errors)


# VALIDACIONES AL ACTUALIZAR

def test_update_expense_negative_amount(client):
    food = create_category(client, "Food")
    created = create_expense(client, 100, "Lunch", "2026-03-18", food["id"])

    response = client.put(f"/expenses/{created['id']}", json={"amount": -10})

    assert response.status_code == 422


def test_update_expense_invalid_date(client):
    food = create_category(client, "Food")
    created = create_expense(client, 100, "Lunch", "2026-03-18", food["id"])

    response = client.put(f"/expenses/{created['id']}", json={"date": "not-a-date"})

    assert response.status_code == 422


def test_update_expense_nonexistent_category(client):
    food = create_category(client, "Food")
    created = create_expense(client, 100, "Lunch", "2026-03-18", food["id"])

    response = client.put(f"/expenses/{created['id']}", json={"category_id": 9999})

    assert response.status_code == 422

