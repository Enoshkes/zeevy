import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import Person, Car, User, Character

# Define an asynchronous fixture for database initialization
@pytest.fixture(scope="function")
async def init_db():
    
    # Create a MongoDB client
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    
    # Initialize Beanie with the database and document models
    await init_beanie(database=client['test_db'], document_models=[User, Character ])
    
    # The yield statement allows the database to be used in tests
    yield
    
    # After yielding, we can perform cleanup operations
    await client.drop_database('test_db')  # Drop the test database after tests
    client.close()  # Close the MongoDB connection
