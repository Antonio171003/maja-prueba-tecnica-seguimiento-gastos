def create_category(client, name="Food"):
    response = client.post("/categories", json={"name": name})
    assert response.status_code == 201
    return response.get_json()


# CREATE

def test_create_expense(client):
    category = create_category(client)

    response = client.post("/expenses", json={
        "amount": 150.50,
        "description": "Groceries",
        "date": "2026-03-18",
        "category_id": category["id"]
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["amount"] == 150.50
    assert data["description"] == "Groceries"
    assert data["date"] == "2026-03-18"
    assert data["category_id"] == category["id"]


def test_create_expense_missing_fields(client):
    response = client.post("/expenses", json={"description": "No amount"})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_expense_no_body(client):
    response = client.post("/expenses")

    assert response.status_code == 400


# LIST

def test_list_expenses_empty(client):
    response = client.get("/expenses")

    assert response.status_code == 200
    body = response.get_json()
    assert body["data"] == []
    assert body["total"] == 0


def test_list_expenses_after_create(client):
    category = create_category(client)
    client.post("/expenses", json={
        "amount": 100.00, "description": "Lunch",
        "date": "2026-03-18", "category_id": category["id"]
    })

    body = client.get("/expenses").get_json()

    assert body["total"] == 1
    assert body["data"][0]["description"] == "Lunch"


def test_filter_expenses_by_category_id(client):
    food = create_category(client, "Food")
    transport = create_category(client, "Transport")

    client.post("/expenses", json={
        "amount": 100.00, "description": "Lunch",
        "date": "2026-03-18", "category_id": food["id"]
    })
    client.post("/expenses", json={
        "amount": 60.00, "description": "Bus",
        "date": "2026-03-18", "category_id": transport["id"]
    })

    body = client.get(f"/expenses?category_id={food['id']}").get_json()

    assert body["total"] == 1
    assert body["data"][0]["description"] == "Lunch"


# GET BY ID

def test_get_expense_by_id(client):
    category = create_category(client)
    created = client.post("/expenses", json={
        "amount": 50.00, "description": "Coffee",
        "date": "2026-03-18", "category_id": category["id"]
    }).get_json()

    response = client.get(f"/expenses/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["description"] == "Coffee"


def test_get_expense_not_found(client):
    response = client.get("/expenses/9999")

    assert response.status_code == 404
    assert "error" in response.get_json()


# UPDATE

def test_update_expense(client):
    category = create_category(client)
    created = client.post("/expenses", json={
        "amount": 50.00, "description": "Coffee",
        "date": "2026-03-18", "category_id": category["id"]
    }).get_json()

    response = client.put(f"/expenses/{created['id']}", json={
        "amount": 75.00,
        "description": "Fancy Coffee"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["amount"] == 75.00
    assert data["description"] == "Fancy Coffee"


def test_update_expense_not_found(client):
    response = client.put("/expenses/9999", json={"amount": 10.00})

    assert response.status_code == 404


def test_update_expense_no_body(client):
    category = create_category(client)
    created = client.post("/expenses", json={
        "amount": 50.00, "description": "Coffee",
        "date": "2026-03-18", "category_id": category["id"]
    }).get_json()

    response = client.put(f"/expenses/{created['id']}")

    assert response.status_code == 400


# DELETE

def test_delete_expense(client):
    category = create_category(client)
    created = client.post("/expenses", json={
        "amount": 50.00, "description": "Coffee",
        "date": "2026-03-18", "category_id": category["id"]
    }).get_json()

    response = client.delete(f"/expenses/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/expenses/{created['id']}").status_code == 404


def test_delete_expense_not_found(client):
    response = client.delete("/expenses/9999")

    assert response.status_code == 404

# FILTROS

def _seed(client):
    """Crea 3 gastos con distintas fechas, montos y categorías."""
    food      = create_category(client, "Food")
    transport = create_category(client, "Transport")

    client.post("/expenses", json={"amount": 100.00, "description": "Lunch",  "date": "2026-03-01", "category_id": food["id"]})
    client.post("/expenses", json={"amount":  60.00, "description": "Bus",    "date": "2026-03-10", "category_id": transport["id"]})
    client.post("/expenses", json={"amount": 200.00, "description": "Dinner", "date": "2026-03-18", "category_id": food["id"]})

    return food, transport


def test_filter_by_start_date(client):
    _seed(client)
    data = client.get("/expenses?start_date=2026-03-10").get_json()["data"]
    assert len(data) == 2
    assert all(e["date"] >= "2026-03-10" for e in data)


def test_filter_by_end_date(client):
    _seed(client)
    data = client.get("/expenses?end_date=2026-03-10").get_json()["data"]
    assert len(data) == 2
    assert all(e["date"] <= "2026-03-10" for e in data)


def test_filter_by_date_range(client):
    _seed(client)
    data = client.get("/expenses?start_date=2026-03-05&end_date=2026-03-15").get_json()["data"]
    assert len(data) == 1
    assert data[0]["description"] == "Bus"


def test_filter_by_category_id(client):
    food, _ = _seed(client)
    data = client.get(f"/expenses?category_id={food['id']}").get_json()["data"]
    assert len(data) == 2
    assert all(e["category_id"] == food["id"] for e in data)


def test_filter_by_min_amount(client):
    _seed(client)
    data = client.get("/expenses?min_amount=100").get_json()["data"]
    assert len(data) == 2
    assert all(e["amount"] >= 100 for e in data)


def test_filter_by_max_amount(client):
    _seed(client)
    data = client.get("/expenses?max_amount=100").get_json()["data"]
    assert len(data) == 2
    assert all(e["amount"] <= 100 for e in data)


def test_filter_by_amount_range(client):
    _seed(client)
    data = client.get("/expenses?min_amount=80&max_amount=150").get_json()["data"]
    assert len(data) == 1
    assert data[0]["description"] == "Lunch"


def test_sort_by_amount_asc(client):
    _seed(client)
    data = client.get("/expenses?sort=amount_asc").get_json()["data"]
    amounts = [e["amount"] for e in data]
    assert amounts == sorted(amounts)


def test_sort_by_amount_desc(client):
    _seed(client)
    data = client.get("/expenses?sort=amount_desc").get_json()["data"]
    amounts = [e["amount"] for e in data]
    assert amounts == sorted(amounts, reverse=True)


def test_sort_by_date_asc(client):
    _seed(client)
    data = client.get("/expenses?sort=date_asc").get_json()["data"]
    dates = [e["date"] for e in data]
    assert dates == sorted(dates)


def test_sort_invalid_value(client):
    response = client.get("/expenses?sort=invalid")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_pagination_limit(client):
    _seed(client)
    body = client.get("/expenses?limit=2&page=1").get_json()
    assert len(body["data"]) == 2
    assert body["total"] == 3
    assert body["pages"] == 2


def test_pagination_page_2(client):
    _seed(client)
    body = client.get("/expenses?limit=2&page=2").get_json()
    assert len(body["data"]) == 1


def test_invalid_numeric_param(client):
    response = client.get("/expenses?min_amount=abc")
    assert response.status_code == 400


def test_invalid_date_format(client):
    response = client.get("/expenses?start_date=18-03-2026")
    assert response.status_code == 400


def test_combined_filters(client):
    food, _ = _seed(client)
    body = client.get(
        f"/expenses?category_id={food['id']}&min_amount=150&sort=amount_desc"
    ).get_json()
    assert body["total"] == 1
    assert body["data"][0]["description"] == "Dinner"