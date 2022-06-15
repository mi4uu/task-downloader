from http import HTTPStatus
import pytest
from httpx import AsyncClient
from backend.schemas import schemas
import asyncio

@pytest.mark.asyncio
async def test_new_file_from_api(client: AsyncClient):
    response = await client.post(  # type: ignore
        "/api/archive/create", json={
            "urls": [
                "https://docs.python.org/3/library/asyncio-task.html",
                "https://jsonplaceholder.typicode.com/todos",
                "https://jsonplaceholder.typicode.com/posts/",
                "https://images.vexels.com/media/users/3/155373/isolated/lists/0fc6a08bcea7d5dabd97ec5b156a3155-sleepy-cat-avatar.png"
                
            ],
            "callback_url": "http://echoserver"
            }
    )

    assert response.status_code == HTTPStatus.CREATED

    id = response.json()["archive_hash"]
    assert id is not None
    await asyncio.sleep(0.1)
    
    response = await client.get(f"/api/archive/status/{id}")
    assert response.json()["status"] in [schemas.Stages.NEW, schemas.Stages.RUNNING]
    
    await asyncio.sleep(15)
    response = await client.get(f"/api/archive/status/{id}")
    
    assert response.json()["status"] in [schemas.Stages.COMPLETED]
    assert response.json()["url"] is not None
    
    response = await client.get(response.json()["url"])
    assert response.headers['content-type'] == 'application/zip'
    


