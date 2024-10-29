from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pyspark.sql import SparkSession
from typing import List
from functools import lru_cache
import logging

# Set up logging for better error handling and debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SparkSession
try:
    spark = SparkSession.builder \
        .appName("PlayersAPI") \
        .getOrCreate()
except Exception as e:
    logger.error(f"Failed to initialize Spark session: {e}")
    raise RuntimeError("Could not initialize Spark session")

# Initialize FastAPI app
app = FastAPI()

# Load CSV with exception handling
try:
    #file_path = "/Users/amirganmor/python/venv_intuit/player.csv"
    # docker
    file_path = "/app/player.csv"
    players_df = spark.read.csv(file_path, header=True, inferSchema=True)
except Exception as e:
    logger.error(f"Error loading CSV file: {e}")
    raise RuntimeError("Failed to load player data")

# Function to get all players with error handling
def get_all_players():
    try:
        players_list = players_df.select("playerID", "nameFirst", "nameLast").collect()
        return [row.asDict() for row in players_list]
    except Exception as e:
        logger.error(f"Error fetching all players: {e}")
        raise HTTPException(status_code=500, detail="Error fetching player data")

# Function to get a player by ID
def get_player_by_id(player_id: str):
    try:
        player = players_df.filter(players_df.playerID == player_id).collect()
        if not player:
            return None
        return player[0].asDict()
    except Exception as e:
        logger.error(f"Error fetching player by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching player data")

# Cache the entire player list
@lru_cache(maxsize=128)
def get_all_players_cached():
    players_list = players_df.select("playerID", "nameFirst", "nameLast").collect()
    return [row.asDict() for row in players_list]
# Endpoint to get all players with optional pagination
@app.get("/api/players", response_model=List[dict])
async def read_players(skip: int = Query(None), limit: int = Query(None)):
    paginated_players = get_all_players_cached()
    # Apply pagination only if skip or limit are provided
    if skip is not None or limit is not None:
        skip = skip or 0  # Default skip to 0 if not provided
        limit = limit or len(paginated_players)  # Default limit to all remaining records if not provided
        paginated_players =  paginated_players[skip:skip + limit]
    # Check if paginated result is empty
    if not paginated_players:
        raise HTTPException(status_code=404, detail="No players found with the given parameters")
    # Return all players if no pagination parameters are provided
    return paginated_players


@app.get("/api/players/{playerID}", response_model=dict)
async def read_player(playerID: str):
    player = get_player_by_id(playerID)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
