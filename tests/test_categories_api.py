def test_create_and_list_categories(client):
    create_payload = {
        "name_ar": "مطاعم",
        "name_en": "Restaurants",
        "icon_url": "https://example.com/icon.png",
        "sort_order": 2,
    }
    create_response = client.post("/api/v1/categories/", json=create_payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] > 0
    assert created["name_en"] == "Restaurants"

    list_response = client.get("/api/v1/categories/")
    assert list_response.status_code == 200
    categories = list_response.json()
    assert len(categories) == 1
    assert categories[0]["id"] == created["id"]


def test_list_categories_sorted_by_sort_order(client):
    client.post(
        "/api/v1/categories/",
        json={"name_ar": "متاحف", "name_en": "Museums", "sort_order": 10},
    )
    client.post(
        "/api/v1/categories/",
        json={"name_ar": "سينما", "name_en": "Cinema", "sort_order": 1},
    )

    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.json()
    assert [row["name_en"] for row in data] == ["Cinema", "Museums"]
