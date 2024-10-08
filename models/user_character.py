from beanie import Document, PydanticObjectId, Link
from models import Character
from pydantic import Field
from typing import List

class User(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    username: str = Field(min_length=3)
    email: str = Field(min_length=3)
    password: str = Field(min_length=3)
    favorite_characters: List[Link["Character"]] = Field(default_factory=list)
    
    class Settings:
        name = "users"
        use_state_management = True 