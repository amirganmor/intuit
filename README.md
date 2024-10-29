# Players API Microservice

This is a FastAPI microservice that serves player data from `player.csv` through two REST API endpoints. The service supports fetching all players with optional pagination and retrieving a single player by ID. 

## Project Structure
- `intuit_final.py`: Contains the main application code, including endpoints for fetching all players and fetching a player by ID.
- `Dockerfile`: Docker configuration file to containerize the application.
- `requirements.txt`: Lists the Python dependencies for the project.
- `test_intuit_final.py`: Contains unit tests for the API using `pytest`.

## Prerequisites
- Python 3.9
- Java (required for PySpark)
- Docker (if you want to containerize the application)

## Setup Instructions

1. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Application Locally**

    ```bash
    uvicorn intuit_final:app --reload
    ```

2. **Run the With Docker**
    ```bash
    docker build -t players_api .
    ```

    ```bash
    docker run -p 8000:8000 -v /Users/amirganmor/python/venv_intuit:/app players_api
    ```

3. **API Endpoints**

    - `GET /api/players`: Returns a list of all players with optional pagination (`skip` and `limit` parameters).
    - `GET /api/players/{playerID}`: Returns details for a single player by `playerID`.

### Sample Requests

- **Get All Players**
    ```bash
    curl -X 'GET' 'http://127.0.0.1:8000/api/players' -H 'accept: application/json'
    ```

- **Get a Single Player by ID**
    ```bash
    curl -X 'GET' 'http://127.0.0.1:8000/api/players/{playerID}' -H 'accept: application/json'
    ```

## Testing
Unit tests for the API endpoints are provided in `test_intuit_final.py`. Run the tests with:
    ```bash
    pytest test_intuit_final.py
    ```
