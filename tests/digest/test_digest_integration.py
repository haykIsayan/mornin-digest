def test_get_digest_returns_404_when_empty(client):
    response = client.get("/digest")
    assert response.status_code == 404

def test_create_digest(client):
    response = client.post(
        "/digest",
        json={"topics": ["technology"]}
    )
    assert response.status_code == 200

    data = response.json()
    assert "articles" in data
    assert data["articles"][0]["topic"] == "technology"