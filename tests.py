import hashlib

import aiohttp
import json


async def test_healthcheck():
    async with aiohttp.ClientSession() as session:
        response = await session.get("http://localhost:8000/healthcheck")
        assert response.status == 200
        assert json.loads(await response.text()) == {}


async def test_hash_string_missing_field():
    async with aiohttp.ClientSession() as session:
        response = await session.post("http://localhost:8000/hash")
        assert response.status == 400
        assert json.loads(await response.text()) == {
            "validation_errors": ["Missing 'string' field"],
        }


async def test_hash_string_valid():
    async with aiohttp.ClientSession() as session:
        data = {"string": "Hello, world!"}
        response = await session.post("http://localhost:8000/hash", json=data)
        assert response.status == 200
        response_json = await response.json()
        hash_string = response_json["hash_string"]
        assert hashlib.sha256(data["string"].encode("utf-8")).hexdigest() == hash_string
