from fastapi.testclient import TestClient
from intuit_final import app

client = TestClient(app)

# Test for fetching all players - should return status code 200 and a list of players
def test_get_all_players():
    response = client.get("/api/players")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list of players
    assert len(response.json()) > 0  # Ensures some players are returned

# Test for fetching a single player by ID (valid ID)
def test_get_single_player_valid_id():
    response = client.get("/api/players/aaronha01")
    assert response.status_code == 200
    assert response.json()["playerID"] == "aaronha01"  # Player with known valid ID

# Test for fetching a single player by ID (invalid ID)
def test_get_single_player_invalid_id():
    response = client.get("/api/players/nonexistent_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found"  # Player ID does not exist

# Test for fetching all players with pagination (limit only)
def test_get_all_players_with_limit():
    response = client.get("/api/players?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5  # Should return only 5 players

# Test for fetching all players with pagination (skip and limit)
def test_get_all_players_with_skip_and_limit():
    response = client.get("/api/players?skip=2&limit=3")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3  # Should return 3 players after skipping the first 2

# Test for invalid pagination parameters (negative skip)
def test_get_all_players_with_invalid_skip():
    response = client.get("/api/players?skip=-1&limit=5")
    assert response.status_code == 404  # FastAPI should return a 404 error for invalid query parameter

# Test for invalid pagination parameters (non-integer values)
def test_get_all_players_with_non_integer_pagination():
    response = client.get("/api/players?skip=two&limit=three")
    assert response.status_code == 422  # FastAPI should return a 422 error for invalid query parameter

# Test for handling a large number of player requests
def test_large_dataset_fetch_all_players():
    response = client.get("/api/players?limit=1000")  # Adjust limit as per the expected dataset size
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 1000  # Confirms handling of large data fetch within limit


# Test for endpoint existence and status for basic health check
def test_api_health_check():
    response = client.get("/api/players")
    assert response.status_code == 200  # Confirms that the endpoint is up and reachable
    assert "application/json" in response.headers["Content-Type"]

