# CREATE

def test_create_category(client):
    response = client.post("/categories", json={"name": "Food"})

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Food"
    assert "id" in data


def test_create_category_missing_name(client):
    response = client.post("/categories", json={})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_category_duplicate(client):
    client.post("/categories", json={"name": "Food"})
    response = client.post("/categories", json={"name": "Food"})

    assert response.status_code == 400
    assert "error" in response.get_json()


# LIST

def test_list_categories_empty(client):
    response = client.get("/categories")

    assert response.status_code == 200
    assert response.get_json() == []


def test_list_categories_after_create(client):
    client.post("/categories", json={"name": "Food"})
    client.post("/categories", json={"name": "Transport"})

    data = client.get("/categories").get_json()

    assert len(data) == 2
    names = {c["name"] for c in data}
    assert names == {"Food", "Transport"}


# GET BY ID

def test_get_category_by_id(client):
    created = client.post("/categories", json={"name": "Food"}).get_json()

    response = client.get(f"/categories/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Food"


def test_get_category_not_found(client):
    response = client.get("/categories/9999")

    assert response.status_code == 404
    assert "error" in response.get_json()


# UPDATE

def test_update_category(client):
    created = client.post("/categories", json={"name": "Food"}).get_json()

    response = client.put(f"/categories/{created['id']}", json={"name": "Groceries"})

    assert response.status_code == 200
    assert response.get_json()["name"] == "Groceries"


def test_update_category_not_found(client):
    response = client.put("/categories/9999", json={"name": "X"})

    assert response.status_code == 404


def test_update_category_duplicate_name(client):
    client.post("/categories", json={"name": "Food"})
    b = client.post("/categories", json={"name": "Transport"}).get_json()

    response = client.put(f"/categories/{b['id']}", json={"name": "Food"})

    assert response.status_code == 400


# DELETE

def test_delete_category(client):
    created = client.post("/categories", json={"name": "Food"}).get_json()

    response = client.delete(f"/categories/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/categories/{created['id']}").status_code == 404


def test_delete_category_not_found(client):
    response = client.delete("/categories/9999")

    assert response.status_code == 404


def test_delete_category_with_expenses(client):
    category = client.post("/categories", json={"name": "Food"}).get_json()
    client.post("/expenses", json={
        "amount": 50.00, "description": "Lunch",
        "date": "2026-03-18", "category_id": category["id"]
    })

    response = client.delete(f"/categories/{category['id']}")

    assert response.status_code == 400
    assert "error" in response.get_json()