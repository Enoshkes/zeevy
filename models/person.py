
from beanie import Document, PydanticObjectId
from typing import Optional
from pydantic import Field, BaseModel, PositiveInt, conint, ConfigDict
from datetime import date

# The Address model defines a structured address, using Pydantic's data validation.
class Address(BaseModel):
    # The city must be a string with a length between 2 and 100 characters.
    city: str = Field(min_length=2, max_length=100)
    
    # The street name must be a string with a length between 3 and 200 characters.
    street_name: str = Field(min_length=3, max_length=200)
    
    # The street number must be a positive integer.
    street_number: PositiveInt
    
    # Configuration allows field names to be used directly, making it easier to work with databases.
    model_config = ConfigDict(populate_by_name=True)

# The Person model represents a document in MongoDB, storing personal information.
class Person(Document):
    # MongoDB will use the '_id' field to store the unique identifier, which is automatically generated.
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    
    # The name field must be a string with at least 3 characters.
    name: str = Field(min_length=3)
    
    # The age field must be a positive integer.
    age: PositiveInt
    
    # The car_id field is optional and stores a reference to a car, if applicable.
    car_id: Optional[PydanticObjectId]
    
    # The address field is structured as an Address object (nested model).
    address: Address
    
    # Define settings specific to the Person collection in MongoDB.
    class Settings:
        # Store Person documents in the "people" collection in MongoDB.
        name = "people"
        
        # Enable state management to track changes in the document.
        use_state_management = True

# The Car model represents a document in MongoDB, storing car information.
class Car(Document):
    # MongoDB will use the '_id' field to store the unique identifier, which is automatically generated.
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id") 
    
    # The brand field must be a string with at least 3 characters.
    brand: str = Field(min_length=3)
    
    # The year field must be an integer between 1980 and the current year.
    year: int = conint(ge=1980, le=date.today().year)
    
    # The color field must be a string with at least 3 characters.
    color: str = Field(min_length=3)
    
    # Define settings specific to the Car collection in MongoDB.
    class Settings:
        # Store Car documents in the "cars" collection in MongoDB.
        name = "cars"
        
        # Enable state management to track changes in the document.
        use_state_management = True