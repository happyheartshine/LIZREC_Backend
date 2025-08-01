from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "sentra_core_db")

# Async client for FastAPI
async_client = None

# Sync client for testing/utilities
sync_client = None

async def connect_to_mongo():
    """Create database connection."""
    global async_client
    try:
        async_client = AsyncIOMotorClient(MONGODB_URL)
        # Test the connection
        await async_client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return async_client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection."""
    global async_client
    if async_client:
        async_client.close()
        print("MongoDB connection closed.")

def get_sync_client():
    """Get synchronous MongoDB client for utilities."""
    global sync_client
    if not sync_client:
        sync_client = MongoClient(MONGODB_URL)
    return sync_client

def get_database():
    """Get database instance."""
    if not async_client:
        raise Exception("Database not connected. Call connect_to_mongo() first.")
    return async_client[DATABASE_NAME]

def get_collection(collection_name: str):
    """Get collection instance."""
    database = get_database()
    return database[collection_name] 