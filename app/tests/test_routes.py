def test_read_all_crystals_returns_empty_list(client):
    # arrange

    # act
    response = client.get("/crystals")
    response_body = response.get_json()
    # assert
    assert response_body == []
    assert response.status_code == 200

def test_read_crystal_by_id(client, make_two_crystals):
    response = client.get("/crystals/2")
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "name": "garnet",
        "color": "red",
        "powers": "protection against evil"
    }

def test_create_crystal(client):
    response = client.post("/crystals", json={
        "name": "tigers eye",
        "color": "brown",
        "powers": "focus the mind"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == "Crystal tigers eye successfully created!"
    