from models import Person, Address
import pytest

# Mark the test as asynchronous using pytest's asyncio marker.
@pytest.mark.asyncio
async def test_person_creation(init_db):
    # Insert a new Person document into the database.
    res = await Person.insert_one(
        Person(
            name='enosh', 
            age=34,  
            address=Address(
                city="rishon", 
                street_name="tsag banot", 
                street_number=43
            ),
            car_id=None
        )
    )
    # Ensure that the insertion result is not None 
    assert res is not None

    
# Mark the test as asynchronous using pytest's asyncio marker.
@pytest.mark.asyncio
async def test_person_read(init_db):
    # Insert a new Person document.
    person = await Person.insert_one(
        Person(
            name='enosh',
            age=34,
            address=Address(
                city="rishon", 
                street_name="tsag banot", 
                street_number=43
            ),
            car_id=None
        )
    )
    
    # Read the Person document using the inserted ID.
    found_person = await Person.get(person.id)
    
    # Assert that the found person is not None and has the correct name.
    assert found_person is not None
    assert found_person.name == 'enosh'
    
# Mark the test as asynchronous using pytest's asyncio marker.
@pytest.mark.asyncio
async def test_person_update(init_db):
    # Insert a new Person document.
    person = await Person.insert_one(
        Person(
            name='enosh',
            age=34,
            address=Address(
                city="rishon", 
                street_name="tsag banot", 
                street_number=43
            ),
            car_id=None
        )
    )
    # Update the person's age.
    await (Person
            .find_one(Person.id == person.id)
            .update({"$set": {"age": 35}}))
    
    # Read the updated document.
    updated_person = await Person.get(person.id)
    
    # Assert that the person's age has been updated to 35.
    assert updated_person.age == 35

# Mark the test as asynchronous using pytest's asyncio marker.
@pytest.mark.asyncio
async def test_person_delete(init_db):
    # Insert a new Person document.
    person = await Person.insert_one(
        Person(
            name='enosh',
            age=34,
            address=Address(
                city="rishon", 
                street_name="tsag banot", 
                street_number=43
            ),
            car_id=None
        )
    )
    
    # Delete the Person document using the inserted ID.
    delete_result = await (Person
            .find_one(Person.id == person.id)
            .delete())
    
    # Assert that one document was deleted.
    assert delete_result.deleted_count == 1
    
    # Try to read the deleted document (should return None).
    deleted_person = await Person.get(person.id)
    
    # Assert that the document is no longer available.
    assert deleted_person is None

# Mark the test as asynchronous using pytest's asyncio marker.
@pytest.mark.asyncio
async def test_find_multiple_people(init_db):
    # Insert multiple Person documents.
    await Person.insert_many([
        Person(
            name='enosh', 
            age=34, 
            address=Address(
                city="rishon", 
                street_name="tsag banot", 
                street_number=43
            ),
            car_id=None
        ),
        Person(
            name='matanel', 
            age=28, 
            address=Address(
                city="tel aviv", 
                street_name="dizengoff", 
                street_number=100
            ),
            car_id=None
        )
    ])
    
    # Find all persons older than 27.
    people_over_27 = await (Person
                .find(Person.age >= 27)
                .to_list())
    
    # Assert that two people are found and that their names are correct.
    assert len(people_over_27) == 2
    assert people_over_27[0].name == 'enosh'
    assert people_over_27[1].name == 'matanel'