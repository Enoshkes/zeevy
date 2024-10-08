import pytest
from models import User, Character
from typing import List
from pydantic import HttpUrl
from beanie.operators import Set, All, And, Or, GT, LT, Eq, In, NotIn

@pytest.mark.asyncio
async def test_create_user_with_favorite_character(init_db):
    character = await Character.insert_one(Character(
        name="Bob Belcher",
        relatives=["Linda Belcher", "Tina Belcher", "Gene Belcher", "Louise Belcher"],
        wiki_url="https://bobsburgers.fandom.com/wiki/Bob_Belcher",
        image="https://bobsburgers-api.herokuapp.com/images/characters/1.jpg",
        gender="Male",
        hair="Black",
        occupation="Restaurant Owner",
        all_occupations=["Restaurant Owner"],
        first_episode="Human Flesh",
        voiced_by="H. Jon Benjamin",
        url="https://bobsburgers-api.herokuapp.com/characters/1"
    ))
    
    user = User(username="bobfan", email="bobfan@example.com", password="password123")
    user.favorite_characters.append(character)
    await user.insert()
    
    fetched_user = await User.get(user.id)
    assert len(fetched_user.favorite_characters) == 1
    x = await fetched_user.favorite_characters[0].fetch()
    
    
@pytest.mark.asyncio
async def test_update_character(init_db):
    character = Character(
        name="Bart Simpson",
        wiki_url="https://simpsons.fandom.com/wiki/Bart_Simpson",
        image="https://static.wikia.nocookie.net/simpsons/images/6/65/Bart_Simpson.png",
        gender="Male",
        first_episode="Good Night",
        voiced_by="Nancy Cartwright",
        url="https://simpsons.fandom.com/wiki/Bart_Simpson"
    )
    await character.insert()
    
    await (Character
           .find_one(Character.name == "Bart Simpson")
           .update(Set({Character.hair: "Yellow"})))
    
    updated_character = await Character.find_one(Character.name == "Bart Simpson")
    assert updated_character.hair == "Yellow"
    
@pytest.mark.asyncio
async def test_delete_character(init_db):
    character = Character(
        name="Lisa Simpson",
        wiki_url="https://simpsons.fandom.com/wiki/Lisa_Simpson",
        image="https://static.wikia.nocookie.net/simpsons/images/e/ec/Lisa_Simpson.png",
        gender="Female",
        first_episode="Good Night",
        voiced_by="Yeardley Smith",
        url="https://simpsons.fandom.com/wiki/Lisa_Simpson"
    )
    await character.insert()
    
    await Character.find_one(Character.name == "Lisa Simpson").delete()
    
    deleted_character = await Character.find_one(Character.name == "Lisa Simpson")
    assert deleted_character is None
    
@pytest.mark.asyncio
async def test_create_user(init_db):
    user = User(
        username="homer_fan",
        email="homer_fan@springfield.com",
        password="doh!123"
    )
    await user.insert()
    
    fetched_user = await User.find_one(User.username == "homer_fan")
    assert fetched_user is not None
    assert fetched_user.email == "homer_fan@springfield.com"
    

@pytest.mark.asyncio
async def test_add_favorite_character(init_db):
    character = Character(
        name="Homer Simpson",
        wiki_url="https://simpsons.fandom.com/wiki/Homer_Simpson",
        image="https://static.wikia.nocookie.net/simpsons/images/b/bd/Homer_Simpson.png",
        gender="Male",
        first_episode="Good Night",
        voiced_by="Dan Castellaneta",
        url="https://simpsons.fandom.com/wiki/Homer_Simpson"
    )
    await character.insert()
    
    user = User(
        username="homer_fan",
        email="homer_fan@springfield.com",
        password="doh!123"
    )
    await user.insert()
    
    await User.find_one(User.username == "homer_fan").update(
        {"$push": {"favorite_characters": character.id}}
    )
    
    updated_user = await User.find_one(User.username == "homer_fan")
    assert len(updated_user.favorite_characters) == 1
    fav_character = await updated_user.favorite_characters[0].fetch()
    assert character.id == fav_character.id 