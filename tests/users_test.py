from models import User
from beanie.operators import In, And, Or, GT, LT, Set, RegEx, NotIn
import pytest

@pytest.mark.asyncio
async def test_user_creation(init_db):
    res = await User.insert_one(
        User(
            username="enosh",
            email="enosh@gmail.com",
            password="1234"
        )
    )
    assert res is not None

@pytest.mark.asyncio
async def test_find_one(init_db):
    await User.insert_one(User(username="alice", email="alice@example.com", password="pass123"))
    user = await User.find_one(User.username == "alice")
    assert user is not None
    assert user.username == "alice"

@pytest.mark.asyncio
async def test_find_many(init_db):
    await User.insert_many([
        User(username="bob", email="bob@example.com", password="pass456"),
        User(username="charlie", email="charlie@example.com", password="pass789")
    ])
    users = await (User
        .find(In(User.username, ["bob", "charlie"]))
        .to_list())
    
    assert len(users) == 2

@pytest.mark.asyncio
async def test_update(init_db):
    await User.insert_one(User(username="david", email="david@example.com", password="oldpass"))
    
    await (User
        .find_one(User.username == "david")
        .update(Set({User.password: "newpass"})))
    
    updated_user = await User.find_one(User.username == "david")
    assert updated_user.password == "newpass"

@pytest.mark.asyncio
async def test_delete(init_db):
    await User.insert_one(User(username="eve", email="eve@example.com", password="pass321"))
    await (User
        .find_one(User.username == "eve")
        .delete())
    
    user = await User.find_one(User.username == "eve")
    assert user is None

@pytest.mark.asyncio
async def test_regex_search(init_db):
    await User.insert_many([
        User(username="frank", email="frank@example.com", password="pass"),
        User(username="freddie", email="freddie@example.com", password="pass")
    ])
    users = await User.find(RegEx(User.username, "^fr")).to_list()
    assert len(users) == 2
    
@pytest.mark.asyncio
async def test_count(init_db):
    await User.insert_many([
        User(username="grace", email="grace@example.com", password="pass"),
        User(username="henry", email="henry@example.com", password="pass")
    ])
    count = await User.find().count()
    assert count == 2
    
@pytest.mark.asyncio
async def test_aggregate(init_db):
    await User.insert_many([
        User(username="ian", email="ian@example.com", password="pass"),
        User(username="jack", email="jack@example.com", password="pass")
    ])
    result = await (User
        .aggregate([
            {"$match": { 'username': { '$regex': 'ian', '$options': 'i'}} },
            { '$project': { '_id': 0, 'username': 1, 'email': 1 }}
        ])
        .to_list())
    
    assert len(result) == 1

@pytest.mark.asyncio
async def test_limit_and_skip(init_db):
    await User.insert_many([
        User(username=f"user{i}", email=f"user{i}@example.com", password="pass")
        for i in range(10)
    ])
    users = await User.find().skip(5).limit(3).to_list()
    assert len(users) == 3
    assert users[0].username == "user5"

@pytest.mark.asyncio
async def test_sort(init_db):
    await User.insert_many([
        User(username="zack", email="zack@example.com", password="pass"),
        User(username="amy", email="amy@example.com", password="pass")
    ])
    users = await User.find().sort(User.username).to_list()
    assert users[0].username == "amy"
    assert users[1].username == "zack"
    
@pytest.mark.asyncio
async def test_complex_query(init_db):
    await User.insert_many([
        User(username="mike", email="mike@example.com", password="pass"),
        User(username="nancy", email="nancy@example.com", password="pass")
    ])
    user = await User.find_one(And(User.username ==  'mike', RegEx(User.email, '^mike', options='i')))
    assert user.username == "mike"
    
@pytest.mark.asyncio
async def test_update_many(init_db):
    await User.insert_many([
        User(username=f"user{i}", email=f"user{i}@example.com", password="oldpass")
        for i in range(5)
    ])
    await User.find(User.password == "oldpass").update_many(Set({User.password: "newpass"}))
    count = await User.find(User.password == "newpass").count()
    assert count == 5

@pytest.mark.asyncio
async def test_delete_many(init_db):
    await User.insert_many([
        User(username=f"temp{i}", email=f"temp{i}@example.com", password="pass")
        for i in range(3)
    ])
    await User.find(RegEx(User.username, "^temp")).delete_many()
    count = await User.find(RegEx(User.username,"^temp")).count()
    assert count == 0
    
@pytest.mark.asyncio
async def test_find_with_or(init_db):
    await User.insert_many([
        User(username="john", email="john@example.com", password="pass"),
        User(username="jane", email="jane@example.com", password="pass")
    ])
    users = await User.find(Or(User.username == "john", User.username == "jane")).to_list()
    assert len(users) == 2

@pytest.mark.asyncio
async def test_not_in(init_db):
    await User.insert_many([
        User(username="user1", email="user1@example.com", password="pass"),
        User(username="user2", email="user2@example.com", password="pass"),
        User(username="admin", email="admin@example.com", password="pass")
    ])
    users = await User.find(NotIn(User.username, ["user1", "user2"])).to_list()
    assert len(users) == 1
    assert users[0].username == "admin"

@pytest.mark.asyncio
async def test_distinct(init_db):
    await User.insert_many([
        User(username="user1", email="user@example.com", password="pass"),
        User(username="user2", email="user@example.com", password="pass"),
        User(username="user3", email="unique@example.com", password="pass")
    ])
    distinct_emails = await User.distinct(User.email)
    assert len(distinct_emails) == 2
    assert "user@example.com" in distinct_emails
    assert "unique@example.com" in distinct_emails