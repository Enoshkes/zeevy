from beanie import Document, PydanticObjectId
from pydantic import Field

class User(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    username: str = Field(min_length=3)
    email: str = Field(min_length=3)
    password: str = Field(min_length=3)
    
    class Settings:
        name = "users"
        use_state_management = True 