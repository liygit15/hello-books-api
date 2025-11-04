import pytest

def test_get_all_genres_with_no_records(client):
    # Act
    response = client.get("/genres")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_genre(client, two_saved_genres):  # We must add the two_saved_genres fixture to our test's parameters. We can comma-separate as many fixtures as this single test needs.
    response = client.get("/genres/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "genre1"
    }


# When we have records, `get_all_genres` returns a list containing a dictionary representing each `genre`
def test_get_all_genres_with_two_records(client, two_saved_genres):
    # Act
    response = client.get("/genres")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "name": "genre1"
    }
    assert response_body[1] == {
        "id": 2,
        "name": "genre2"
    }

# When we have records and a `title` query in the request arguments, `get_all_genres` returns a list containing only the `genre`s that match the query
def test_get_all_genres_with_name_query_matching_none(client, two_saved_genres):
    # Act
    data = {'name': 'Desert genre'}
    response = client.get("/genres", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# When we have records and a `title` query in the request arguments, `get_all_genres` returns a list containing only the `genre`s that match the query
def test_get_all_genres_with_name_query_matching_one(client, two_saved_genres):
    # Act
    data = {'name': 'genre1'}
    response = client.get("/genres", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "name": "genre1"
    }


# When we call `get_one_genre` with a numeric ID that doesn't have a record, we get the expected error message
def test_get_one_genre_missing_record(client, two_saved_genres):
    # Act
    response = client.get("/genres/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Genre 3 not found"}

# When we call `get_one_genre` with a non-numeric ID, we get the expected error message
def test_get_one_genre_invalid_id(client, two_saved_genres):
    # Act
    response = client.get("/genres/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Genre cat invalid"}

def test_create_one_genre(client):
    # Act
    response = client.post("/genres", json={
        "name": "New genre",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "New genre",
    }

def test_create_one_genre_no_name(client):
    # Arrange
    test_data = {}

    # Act 
    response = client.post("/genres", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing name'}


def test_create_one_genre_with_extra_keys(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "genre1",
        "description": "The Best!",
    }

    # Act
    response = client.post("/genres", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "genre1"
    }


def test_update_genre(client, two_saved_genres):
    # Arrange
    test_data = {
        "name": "update genre",
    }

    # Act
    response = client.put("/genres/1", json=test_data)

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_update_genre_with_extra_keys(client, two_saved_genres):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "genre1",
        "description": "The Best!",
    }

    # Act
    response = client.put("/genres/1", json=test_data)

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_update_genre_missing_record(client, two_saved_genres):
    # Arrange
    test_data = {}

    # Act
    response = client.put("/genres/3", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Genre 3 not found"}

def test_update_genre_invalid_id(client, two_saved_genres):
    # Arrange
    test_data = {
        "name": "New genre",
    }

    # Act
    response = client.put("/genres/cat", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Genre cat invalid"}

def test_delete_genre(client, two_saved_genres):
    # Act
    response = client.delete("/genres/1")

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_delete_genre_missing_record(client, two_saved_genres):
    # Act
    response = client.delete("/genres/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Genre 3 not found"}

def test_delete_genre_invalid_id(client, two_saved_genres):
    # Act
    response = client.delete("/genres/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Genre cat invalid"}