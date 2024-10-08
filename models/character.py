from beanie import Document, Indexed, PydanticObjectId
from pydantic import HttpUrl, Field
from typing import List, Optional

class Character(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    name: str
    relatives: List[str] = Field(default_factory=list)
    wiki_url: HttpUrl = Field(alias="wikiUrl")
    image: HttpUrl
    gender: str
    hair: Optional[str] = None
    occupation: Optional[str] = None
    all_occupations: List[str] = Field(default_factory=list, alias="allOccupations")
    first_episode: str = Field(alias="firstEpisode")
    voiced_by: str = Field(alias="voicedBy")
    url: HttpUrl

    class Settings:
        name = "characters" 
        use_state_management = True
    