
def test_read_main(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

    response = test_client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
